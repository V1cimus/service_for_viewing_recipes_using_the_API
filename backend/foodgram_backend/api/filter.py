from django_filters import rest_framework

from recipes.models import Recipe, Tag


class RecipeFilter(rest_framework.FilterSet):
    tags = rest_framework.filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    is_favorited = rest_framework.filters.NumberFilter(
        method="filter_is_favorite",
    )
    is_in_shopping_cart = rest_framework.filters.NumberFilter(
        method="filter_is_shopping_card",
    )

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def filter_is_favorite(self, queryset, name, value):
        if value:
            return queryset.filter(
                favorite_subscribed_recipe__subscriber=self.request.user
            )
        return queryset

    def filter_is_shopping_card(self, queryset, name, value):
        if value:
            return queryset.filter(
                shoppinglist_subscribed_recipe__subscriber=self.request.user
            )
        return queryset
