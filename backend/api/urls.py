from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                       UserSubscriptionViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register(r'users', UserSubscriptionViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
