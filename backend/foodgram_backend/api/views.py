from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from .filter import BaseIngredientFilter, RecipeFilter
from .permissions import (
    AuthorPermission,
    IsAdminOrReadOnlyPermission,
    IsNotBanPermission,
)
from .serializers import (
    AuthorSubscriptionSerializer,
    BaseIngredientSerializer,
    CreateRecipeSerializer,
    FavoriteSerializer,
    RecipeSerializer,
    ShoppingListSerializer,
    TagSerializer,
)
from .util import start_download_shopping_cart
from .viewsets import CreateAndDestroyViewSet, GetAuthorSubViewSet
from recipes.models import BaseIngredient, Ingredient, Recipe, Tag
from users.models import Subscription

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра списка тегов.
    """
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class BaseIngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Базовый ViewSet для просмотра списка ингредиентов.
    Поддерживает фильтрацию по названию ингредиента.
    """

    queryset = BaseIngredient.objects.all()
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = None
    serializer_class = BaseIngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BaseIngredientFilter


class GetAuthorSubscriptionViewSet(GetAuthorSubViewSet):
    """
    ViewSet для просмотра подписок пользователя на авторов.
    """

    permission_classes = (IsAuthenticated, IsNotBanPermission)
    serializer_class = AuthorSubscriptionSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class AuthorSubscriptionViewSet(CreateAndDestroyViewSet):
    """
    ViewSet для создания и удаления подписки пользователя на автора.
    """

    permission_classes = (IsAuthenticated, IsNotBanPermission)
    serializer_class = AuthorSubscriptionSerializer

    def destroy(self, request, *args, **kwargs):
        serializer = AuthorSubscriptionSerializer(
            context={"request": request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели создания, просмотра,
    редактирования и удаления рецептов.

    Предоставляет CRUD-функционал для модели Recipe и
    дополнительные методы для добавления/удаления избранных рецептов
    и продуктов в/из список(а) покупок.
    """

    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        if self.request.method == "GET":
            return (
                IsAuthenticatedOrReadOnly(),
                IsNotBanPermission(),
            )
        elif self.request.method in ("PATCH", "DELETE",):
            return (
                AuthorPermission(),
                IsNotBanPermission(),
            )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return CreateRecipeSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.context["request"] = self.request
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.context["request"] = self.request
        serializer.save(author=self.request.user)

    @action(
        methods=("POST", "DELETE", ),
        detail=True,
        url_path="favorite",
        permission_classes=(IsAuthenticated,),
    )
    def create_destroy_favorite(self, request, pk=None):
        serializer = FavoriteSerializer(
            context={"request": request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            serializer.validated_data.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=("POST", "DELETE", ),
        detail=True,
        url_path="shopping_cart",
        permission_classes=(IsAuthenticated,),
    )
    def create_destroy_shopping_cart(self, request, pk=None):
        serializer = ShoppingListSerializer(
            context={"request": request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            serializer.validated_data.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=("GET", ),
        detail=False,
        url_path="download_shopping_cart",
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients_list = (
            Ingredient.objects.prefetch_related("ingredient").filter(
                to_recipe__shoppinglist_subscribed_recipe__subscriber=user
            ).values(
                "ingredient",
                name=F("ingredient__name"),
                measurement_unit=F("ingredient__measurement_unit"),
            )
            .annotate(total_amount=Sum("amount"))
        )
        return start_download_shopping_cart(ingredients_list)
