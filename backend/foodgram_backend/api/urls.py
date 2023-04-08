from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AuthorSubscriptionViewSet,
    BaseIngredientsViewSet,
    GetAuthorSubscriptionViewSet,
    RecipeViewSet,
    TagViewSet,
)

v1_router = DefaultRouter()
v1_router.register(
    "users/subscriptions",
    GetAuthorSubscriptionViewSet,
    basename="subscriptions",
)
v1_router.register(
    r"users/(?P<user_id>\d+)/subscribe",
    AuthorSubscriptionViewSet,
    basename="subscribe",
)
v1_router.register("recipes", RecipeViewSet)
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
