from django.contrib import admin

from .models import (
    Recipe, Tag, Ingredients, BaseIngredients, Unit, Favorite, ShoppingList
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "name",
        "get_favorites_count",
    )
    list_filter = ("author", "name", "tags",)
    filter_horizontal = ("tags", "ingredients")
    empty_value_display = "---пусто---"

    def get_favorites_count(self, obj):
        return obj.favorite_subscribed_recipe.count()


@admin.register(BaseIngredients)
class BaseIngredientsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "---пусто---"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "color",
    )
    list_filter = ("name",)
    empty_value_display = "---пусто---"


admin.site.register(Favorite)
admin.site.register(Ingredients)
admin.site.register(Unit)
admin.site.register(ShoppingList)
