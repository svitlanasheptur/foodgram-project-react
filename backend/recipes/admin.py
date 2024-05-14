from django.contrib import admin
from django.db.models import Count
from import_export.admin import ImportExportModelAdmin

from core.resources import IngredientResource
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


class TagInline(admin.StackedInline):
    model = Recipe.tags.through
    extra = 0
    min_num = 1


class IngredientInline(admin.StackedInline):
    model = Recipe.ingredients.through
    extra = 0
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
        "slug",
    )
    search_fields = (
        "name",
        "slug",
    )


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    resource_classes = [IngredientResource]
    list_display = (
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
        "favorite_count",
    )
    search_fields = (
        "name",
        "author__username",
    )
    list_filter = (
        "name",
        "author",
    )
    exclude = ("tags",)
    inlines = (
        IngredientInline,
        TagInline,
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(favorite_count=Count("favorite"))
        return queryset

    def favorite_count(self, obj):
        return obj.favorite_count

    favorite_count.admin_order_field = "favorite_count"
    favorite_count.short_description = "В избранном"


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )
    search_fields = ("user",)


@admin.register(Favorite)
class FavotiteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )
    search_fields = ("user",)


admin.site.empty_value_display = "Отсутствует"
