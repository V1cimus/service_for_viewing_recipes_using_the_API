from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    TagViewSet,
    BaseIngredientsViewSet,
    GetAuthorSubViewSet,
    AuthorSubscriptionViewSet,
    AddInFavoriteShoppingViewSet,
    RecipeViewSet
)

v1_router = DefaultRouter()
v1_router.register(
    "users/subscriptions",
    GetAuthorSubViewSet,
    basename="subscriptions",
    )
v1_router.register(
    r"users/(?P<user_id>\d+)/subscriptions",
    AuthorSubscriptionViewSet,
    basename="subscriptions",
    )
v1_router.register("recipes", RecipeViewSet)
v1_router.register(
    r"recipes/(?P<recipe_id>\d+)/favorite",
    AddInFavoriteShoppingViewSet,
    basename="favorite",
    )
v1_router.register(
    r"recipes/(?P<recipe_id>\d+)/shopping_cart",
    AddInFavoriteShoppingViewSet,
    basename="shopping_cart",
    )
v1_router.register("tags", TagViewSet)
v1_router.register(
    "ingredients",
    BaseIngredientsViewSet,
    basename="ingredients",
)

urlpatterns = [
    path("", include(v1_router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
