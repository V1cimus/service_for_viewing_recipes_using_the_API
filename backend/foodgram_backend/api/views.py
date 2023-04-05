from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated,
)

from django.db.models import Case, When, Sum, F
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    TagSerializer,
    BaseIngredientsSerializer,
    AuthorSubSerializer,
    ShortRecipesSerializer,
    AddInSerializer,
    RecipeSerializer,
    CreateRecipeSerializer,
)
from posts.models import Tag, BaseIngredients, Recipe, Ingredients
from users.models import SubscribAuthor
from .viewsets import GetAuthorSubViewSet, CreateAndDectroyViewSet
from .filter import RecipeFilter
from .util import start_download_shopping_cart
from .permissions import IsNotBanPermission, AuthorPermission


User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра списка тегов.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class BaseIngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Базовый ViewSet для просмотра списка ингредиентов.
    Поддерживает фильтрацию по названию ингредиента.
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
    serializer_class = BaseIngredientsSerializer

    def get_queryset(self):
        queryset = BaseIngredients.objects.all()
        name = self.request.query_params.get("name", None)
        if name:
            queryset = (
                queryset.filter(name__icontains=name.lower())
                .annotate(order=Case(When(name__istartswith=name, then=1)))
                .order_by("order", "name")
            )
        return queryset


class GetAuthorSubViewSet(GetAuthorSubViewSet):
    """
    ViewSet для просмотра подписок пользователя на авторов.
    """

    permission_classes = (IsAuthenticated, IsNotBanPermission)
    serializer_class = AuthorSubSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return User.objects.filter(subscribing__user=self.request.user)


class AuthorSubscriptionViewSet(CreateAndDectroyViewSet):
    """
    ViewSet для создания и удаления подписки пользователя на автора.
    """

    permission_classes = (IsAuthenticated, IsNotBanPermission)

    def create(self, request, *args, **kwargs):
        serializer = AuthorSubSerializer(
            context={"request": request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        subscriber, subscribing = serializer.validated_data
        SubscribAuthor.objects.create(
            user=subscriber,
            author=subscribing,
        )
        serializer = AuthorSubSerializer(
            context={"request": request},
            instance=subscribing,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        serializer = AuthorSubSerializer(
            context={"request": request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return SubscribAuthor.objects.filter(user=self.request.user)


class AddInFavoriteShoppingViewSet(CreateAndDectroyViewSet):
    """
    ViewSet для подписки на избранные рецепты и
    добавление рецептов в список покупок.
    Пользователи могут добавлять рецепты и удалять их.
    """

    queryset = Recipe.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = AddInSerializer(
            context={"request": request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = ShortRecipesSerializer(
            instance=serializer.validated_data.get("subscribed_recipe")
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        serializer = AddInSerializer(
            context={"request": request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.delete()
        return Response({}, status=status.HTTP_201_CREATED)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели создания, просмотра,
    редактирования и удаления рецептов.
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
        if self.request.method == "PATCH":
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
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        serializer.context["request"] = self.request
        serializer.save(author=self.request.user)
        return super().perform_update(serializer)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
        url_path="download_shopping_cart",
    )
    def download_shopping_cart(self, request):
        ingredients_list = (
            Ingredients.objects.filter(
                recipe__shoppinglist_subscribed_recipe__subscriber=request.user
            )
            .values(
                "ingredients",
                name=F("ingredients__name"),
                measurement_unit=F("ingredients__measurement_unit__name"),
            )
            .annotate(total_amount=Sum("amount"))
        )
        return start_download_shopping_cart(ingredients_list)
