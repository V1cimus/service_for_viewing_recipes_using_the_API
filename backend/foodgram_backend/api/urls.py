from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import (
    AuthorSubscriptionViewSet,
    BaseIngredientsViewSet,
    GetAuthorSubscriptionViewSet,
    RecipeViewSet,
    TagViewSet,
)

schema_view = get_schema_view(
    openapi.Info(
        title='API FoodGram',
        default_version='V1.0',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
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
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
]
