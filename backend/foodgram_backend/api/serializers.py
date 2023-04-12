from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ValidationError

from .validators import is_unique, min_value_validator, validate_subscription
from recipes.models import (
    BaseIngredient,
    Favorite,
    Ingredient,
    Recipe,
    ShoppingList,
    Tag,
)
from users.models import Subscription

User = get_user_model()


class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для кратких данных о рецептах,
    используется для вывода списка рецептов.
    """

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )
        read_only_fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для данных пользователей,
    используется для вывода списка пользователей
    и информации о конкретном пользователе.
    Метод get_is_subscribed: определение,
    подписан ли текущий пользователь на конкретного пользователя.
    """

    is_subscribed = SerializerMethodField(
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        request = self.context["request"]
        if request.user.is_anonymous:
            return False
        return obj.subscribing.filter(user=request.user).exists()


class UserCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для создания новых пользователей,
    используется при регистрации новых пользователей.
    """

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для тегов рецептов,
    используется для вывода списка тегов.
    """

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "color",
            "slug",
        )
        read_only_fields = (
            "id",
            "name",
            "color",
            "slug",
        )


class BaseIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для базовых ингредиентов рецептов,
    используется для вывода списка базовых ингредиентов.
    """

    class Meta:
        model = BaseIngredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )
        read_only_fields = (
            "id",
            "name",
            "measurement_unit",
        )


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингредиентов рецепта.
    Выводит информацию о базовом ингредиенте и его количестве в рецепте.
    """

    name = serializers.ReadOnlyField(
        source="ingredient.name",
    )
    measurement_unit = serializers.CharField(
        read_only=True,
        source="ingredient.measurement_unit",
        required=False,
    )
    id = serializers.IntegerField(
        required=True,
    )
    amount = serializers.IntegerField(required=True,)

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )
        read_only_fields = (
            "id",
            "measurement_unit",
            "name",
        )


class AuthorSubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения информации об авторе рецептов и их количестве,
    а также для подписки/отписки на автора.

    Методы:
    - get_recipes_count: метод, который возвращает количество рецептов у автора
    - get_recipes: метод, который возвращает список рецептов автора
    - get_author: метод, который возвращает информацию об авторе
    """

    author = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            "author",
            "recipes",
            "recipes_count",
        )
        read_only_fields = (
            "author",
            "recipes",
            "recipes_count",
        )

    def get_recipes_count(self, obj):
        return obj.author.author_recipe.count()

    def get_recipes(self, obj):
        request = self.context["request"]
        limit = request.query_params.get("recipes_limit", 6)
        recipes = obj.author.author_recipe.all()
        recipes = recipes[:int(limit)]
        serializer = ShortRecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data

    def get_author(self, obj):
        request = self.context["request"]
        serializer = UserSerializer(
            obj.author, context={'request': request}, read_only=True
        )
        return serializer.data

    def validate(self, data):
        request = self.context.get("request")
        subscriber = request.user
        subscribing = get_object_or_404(
            User, pk=request.parser_context.get("kwargs").get("user_id")
        )
        subscrib_author = Subscription.objects.filter(
            user=subscriber, author=subscribing
        )

        if subscriber == subscribing:
            raise ValidationError(
                detail={
                    "errors": (
                        "Вы не можете подписаться(отписаться)"
                        " на(от) самого себя!"
                    )
                },
                code=status.HTTP_400_BAD_REQUEST,
            )

        if request.method == "POST":
            if subscrib_author.exists():
                raise ValidationError(
                    detail={"errors": "Вы уже подписаны на данного автора!"},
                    code=status.HTTP_400_BAD_REQUEST,
                )
            data = {
                "user": subscriber,
                "author": subscribing,
            }
            return data

        if request.method == "DELETE":
            if not subscrib_author.exists():
                raise ValidationError(
                    detail={"errors": "Вы не подписаны на данного автора!"},
                    code=status.HTTP_404_NOT_FOUND,
                )
            return subscrib_author

    def to_representation(self, instance):
        data = super().to_representation(instance)
        new_data = data.pop("author")
        new_data.update(data)
        return new_data


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления/удаления
    рецепта в/из избранное.
    """

    subscriber = UserSerializer(required=False)
    subscribed_recipe = ShortRecipeSerializer(required=False)

    class Meta:
        model = Favorite
        fields = ("subscriber", "subscribed_recipe")

    def validate(self, data):
        request = self.context["request"]
        subscribed_recipe = get_object_or_404(
            Recipe, id=request.parser_context.get("kwargs").get("pk")
        )
        binding_recipe = Favorite.objects.filter(
            subscribed_recipe=subscribed_recipe, subscriber=request.user
        )
        return validate_subscription(
            request, binding_recipe, subscribed_recipe
        )

    def to_representation(self, instance):
        return ShortRecipeSerializer(instance.subscribed_recipe).data


class ShoppingListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления/удаления
    рецепта в/из список покупок.
    """

    subscriber = UserSerializer(required=False)
    subscribed_recipe = ShortRecipeSerializer(required=False)

    class Meta:
        model = ShoppingList
        fields = ("subscriber", "subscribed_recipe")

    def validate(self, data):
        request = self.context["request"]
        subscribed_recipe = get_object_or_404(
            Recipe, id=request.parser_context.get("kwargs").get("pk")
        )
        binding_recipe = ShoppingList.objects.filter(
            subscribed_recipe=subscribed_recipe, subscriber=request.user
        )
        return validate_subscription(
            request, binding_recipe, subscribed_recipe
        )

    def to_representation(self, instance):
        return ShortRecipeSerializer(instance.subscribed_recipe).data


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Recipe, который возвращает полную
    информацию о рецепте, включая информацию об авторе, тегах,
    ингредиентах, а также флаги is_favorited и is_in_shopping_cart.

    Методы:
    - get_tags: метод, который возвращает список тегов рецепта
    - get_ingredients: метод, который возвращает список
    ингредиентов рецепта
    - to_internal_value: метод, который декодирует base64-кодированную
    строку в изображение
    - get_is_favorited: метод, который возвращает флаг, показывающий,
    добавлен ли рецепт в избранное у текущего пользователя
    - get_is_in_shopping_cart: метод, который возвращает флаг,
    показывающий, есть ли рецепт в списке покупок текущего пользователя
    """

    author = UserSerializer(
        read_only=True,
        many=False,
    )
    tags = SerializerMethodField()
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "text",
            "id",
            "name",
            "image",
            "cooking_time",
        )
        read_only_fields = ("is_favorited", "is_in_shopping_cart")

    def get_tags(self, obj):
        serializer = TagSerializer(obj.tags.all(), many=True, read_only=True)
        return serializer.data

    def get_ingredients(self, obj):
        ingredients = Ingredient.objects.select_related(
            "to_recipe").filter(to_recipe=obj)
        serializer = IngredientSerializer(
            ingredients,
            many=True,
            read_only=True,
        )
        return serializer.data

    def get_is_favorited(self, obj):
        request = self.context["request"]
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            subscribed_recipe=obj, subscriber=request.user
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context["request"]
        if request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(
            subscribed_recipe=obj, subscriber=request.user
        ).exists()


class CreateRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Recipe, который используется
    для создания и обновления рецепта.

    Методы:
    - validate_tags: метод, который проверяет, что введенные
    теги уникальны и существуют в базе данных.
    - validate_ingredients: метод, который проверяет, что
    введенные ингредиенты уникальны и существуют в базе данных.
    - is_unique: метод, который проверяет, что элементы списка уникальны.
    - create: метод, который создает новый объект рецепта,
    а также связанные с ним теги и ингредиенты.
    - update: метод, который обновляет существующий объект рецепта,
    а также связанные с ним теги и ингредиенты.
    - get_ingredients_list_object: метод, который получает список
    ингредиентов рецепта и создает объекты модели Ingredients,
    которые связываются с объектом рецепта и базовыми ингредиентами,
    указанными в списке ингредиентов.
    """

    author = UserSerializer(
        read_only=True,
        many=False,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        error_messages={
            "error": "Один или несколько введенных Тегов не существуют!"
        },
    )
    ingredients = IngredientSerializer(
        many=True,
    )
    image = Base64ImageField(max_length=None)
    name = serializers.CharField()
    cooking_time = serializers.IntegerField()

    class Meta(ShortRecipeSerializer.Meta):
        model = Recipe
        fields = (
            "tags",
            "author",
            "ingredients",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def validate_cooking_time(self, cooking_time):
        min_value_validator(cooking_time, "Время приготовления",)
        return cooking_time

    def validate_tags(self, tags):
        is_unique(tags, "Теги")
        return tags

    def validate_ingredients(self, ingredients):
        for ingredient in ingredients:
            if not BaseIngredient.objects.filter(
                    pk=ingredient.get("id")).exists():
                raise ValidationError(
                    detail={
                        "errors": (
                            "Один или несколько введенных "
                            "Ингредиентов не существуют!"
                        )
                    },
                    code=status.HTTP_404_NOT_FOUND,
                )
        return ingredients

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        is_unique(ingredients, "Ингредиенты")
        tags = validated_data.pop("tags")
        for ingredient in ingredients:
            min_value_validator(ingredient.get("amount"), "Количество",)
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.ingredients.set(
            self.get_ingredients_list_object(ingredients, recipe)
        )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        instance.tags.set(tags)
        instance.ingredients.set(
            self.get_ingredients_list_object(ingredients, instance)
        )
        return super().update(instance, validated_data)

    def get_ingredients_list_object(self, ingredients, recipe):
        exist_ingredients = recipe.ingredients.all()
        ingredients_as_object = []
        for ingredient in ingredients:
            amount = ingredient.get("amount")
            ingredient = BaseIngredient.objects.get(
                    pk=ingredient.get("id")
                )
            if ingredient in exist_ingredients:
                ingredient_obj = Ingredient.objects.get(
                    ingredient=ingredient,
                    to_recipe=recipe,
                )
                ingredient_obj.amount = amount
            else:
                ingredient_obj = Ingredient.objects.create(
                    ingredient=ingredient,
                    to_recipe=recipe,
                    amount=amount,
                )
            ingredient_obj.save()
            ingredients_as_object.append(ingredient.id)
        return ingredients_as_object

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance, context=self.context)
        return serializer.data
