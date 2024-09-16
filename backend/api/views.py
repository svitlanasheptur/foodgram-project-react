import django_filters
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import LimitPageNumberPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (FavoriteCreateSerializer, IngredientSerializer,
                             RecipeCreateAndUpdateSerializer,
                             RecipeReadSerializer,
                             ShoppingCartCreateSerializer,
                             SubscribeCreateSerializer, TagSerializer)
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Subscription


class UserSubscriptionViewSet(UserViewSet):
    """Вьюсет для работы с пользователями и подписками."""

    pagination_class = LimitPageNumberPagination
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == 'me':
            return [IsAuthenticated()]
        return super(UserSubscriptionViewSet, self).get_permissions()

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, *args, **kwargs):
        author = self.get_object()
        user = request.user

        serializer = SubscribeCreateSerializer(
            data={'user': user.username, 'author': author.id},
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, *args, **kwargs):
        author = self.get_object()

        count_delete_subscribe, _ = Subscription.objects.filter(
            user=request.user, author=author
        ).delete()

        if not count_delete_subscribe:
            return Response(
                {'errors': 'Вы не подписаны на данного пользователя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        queryset = Subscription.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeCreateSerializer(
            pages,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для получения тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitPageNumberPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateAndUpdateSerializer

    def get_permissions(self):
        if self.action in [
            'favorite', 'shopping_cart', 'download_shopping_cart'
        ]:
            return [IsAuthenticated()]
        return super().get_permissions()

    def add_item(self, serializer_type, request, pk):
        serializer = serializer_type(
            data={'recipe': pk}, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_item(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        count_delete_item, _ = model.objects.filter(
            user=request.user, recipe=recipe
        ).delete()

        if not count_delete_item:
            return Response(
                {'errors': 'Невозможно удалить, сначала добавьте'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST'],
        url_path='favorite',
        url_name='favorite',
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        return self.add_item(FavoriteCreateSerializer, request, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return self.delete_item(Favorite, request, pk)

    @action(
        detail=True,
        methods=['POST'],
        url_path='shopping_cart',
        url_name='shopping_cart',
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        return self.add_item(ShoppingCartCreateSerializer, request, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return self.delete_item(ShoppingCart, request, pk)

    def get_shopping_list_data(self, user):
        return (
            ShoppingCart.objects.filter(user=user)
            .values('recipe')
            .values_list(
                'recipe__ingredients__name',
                'recipe__ingredients__measurement_unit',
            )
            .annotate(total_amount=Sum('recipe__ingredientes__amount'))
        )

    def format_shopping_list(self, ingredients):
        shopping_list = ['Список покупок\n']
        for i, ingredient in enumerate(ingredients, start=1):
            shopping_list.append(
                f'{i}. {ingredient[0].capitalize()} '
                f'({ingredient[1]}) - {ingredient[2]}\n'
            )
        return ''.join(shopping_list)

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        ingredients = self.get_shopping_list_data(request.user)
        shopping_list_text = self.format_shopping_list(ingredients)

        response = HttpResponse(shopping_list_text, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )

        return response


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для получения ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = None
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = IngredientFilter
    search_fields = ('name',)
