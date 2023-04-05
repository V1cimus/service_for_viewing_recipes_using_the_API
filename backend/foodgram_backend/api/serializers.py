from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ValidationError

from posts.models import (
    Tag,
    BaseIngredients,
    Recipe,
    Favorite,
    Ingredients,
    ShoppingList,
)
from users.models import SubscribAuthor

User = get_user_model()


class ShortRecipesSerializer(serializers.ModelSerializer):
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


class UsersSerializer(serializers.ModelSerializer):
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
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return obj.subscribing.filter(user=request.user).exists()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания новых пользователей,
    используется при регистрации новых пользователей.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password'),
        )
        return user


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


class BaseIngredientsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для базовых ингредиентов рецептов,
    используется для вывода списка базовых ингредиентов.
    """

    measurement_unit = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = BaseIngredients
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


class IngredientsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингредиентов рецепта.
    Выводит информацию о базовом ингредиенте и его количестве в рецепте.

    Методы:
    - get_amount: метод, который возвращает количественое значение ингредиента
    - to_representation: метод, который сериализует объект базового ингредиента
    и добавляет к нему количество ингредиента в рецепте.
    """

    name = serializers.ReadOnlyField(
        source="ingredients.name",
    )
    measurement_unit = serializers.CharField(
        read_only=True,
        source="ingredients.measurement_unit",
        required=False,
    )
    id = serializers.IntegerField(
        required=True,
    )

    class Meta:
        model = Ingredients
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


class AuthorSubSerializer(UsersSerializer):
    """
    Сериализатор для получения информации об авторе рецептов и их количестве,
    а также для подписки/отписки на автора.

    Методы:
    - get_recipes_count: метод, который возвращает количество рецептов у автора
    - get_recipes: метод, который возвращает список рецептов автора
    """

    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta(UsersSerializer.Meta):
        fields = UsersSerializer.Meta.fields + (
            "recipes",
            "recipes_count",
        )
        read_only_fields = UsersSerializer.Meta.fields + (
            "recipes",
            "recipes_count",
        )

    def get_recipes_count(self, obj):
        return obj.author_recipe.count()

    def get_recipes(self, obj):
        request = self.context.get("request")
        limit = request.query_params.get("recipes_limit")
        recipes = obj.author_recipe.all()
        if limit:
            recipes = recipes[: int(limit)]
        serializer = ShortRecipesSerializer(recipes, many=True, read_only=True)
        return serializer.data

    def validate(self, data):
        request = self.context.get("request")
        subscriber = request.user
        subscribing = get_object_or_404(
            User, pk=request.parser_context.get("kwargs").get("user_id")
        )
        subscrib_author = SubscribAuthor.objects.filter(
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
            return subscriber, subscribing
        if request.method == "DELETE":
            if not subscrib_author.exists():
                raise ValidationError(
                    detail={"errors": "Вы не подписаны на данного автора!"},
                    code=status.HTTP_400_BAD_REQUEST,
                )
            return subscrib_author


class AddInSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления/удаления
    рецепта в/из избранного/списка покупок.
    """

    ENTITY_TO_MODEL = {
        "favorite": Favorite,
        "shopping_cart": ShoppingList,
    }
    subscriber = UsersSerializer(required=False)
    subscribed_recipe = ShortRecipesSerializer(required=False)

    class Meta:
        model = None
        fields = ("subscriber", "subscribed_recipe")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.model = self.__get_current_model()[0]

    def validate(self, data):
        request = self.context.get("request")
        subscribed_recipe = get_object_or_404(
            Recipe, id=request.parser_context.get("kwargs").get("recipe_id")
        )
        FavoriteOrShoppingList, current_name = self.__get_current_model()
        binding_recipe = FavoriteOrShoppingList.objects.filter(
            subscribed_recipe=subscribed_recipe, subscriber=request.user
        )
        if request.method == "POST":
            if binding_recipe.exists():
                raise ValidationError(
                    detail={
                        "errors": f"Рецепт уже добавлен в {current_name}!"
                    },
                    code=status.HTTP_400_BAD_REQUEST,
                )
            data = {
                "subscriber": request.user,
                "subscribed_recipe": subscribed_recipe,
            }
            return data
        if request.method == "DELETE":
            if not binding_recipe.exists():
                raise ValidationError(
                    detail={"errors": f"Рецепт не добавлен в {current_name}!"},
                    code=status.HTTP_400_BAD_REQUEST,
                )
            return binding_recipe

    def __get_current_model(self):
        request = self.context.get("request")
        current_name = request.build_absolute_uri().split("/")[-2]
        return self.ENTITY_TO_MODEL.get(current_name), current_name


class RecipeSerializer(ShortRecipesSerializer):
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

    author = UsersSerializer(
        read_only=True,
        many=False,
    )
    tags = SerializerMethodField()
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta(ShortRecipesSerializer.Meta):
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "text",
        ) + ShortRecipesSerializer.Meta.fields
        read_only_fields = ("author", "is_favorited", "is_in_shopping_cart")

    def get_tags(self, obj):
        serializer = TagSerializer(obj.tags.all(), many=True, read_only=True)
        return serializer.data

    def get_ingredients(self, obj):
        serializer = IngredientsSerializer(
            obj.ingredients.all(), many=True, read_only=True
        )
        return serializer.data

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            subscribed_recipe=obj, subscriber=request.user
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
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

    author = UsersSerializer(
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
    ingredients = IngredientsSerializer(
        many=True,
    )
    image = Base64ImageField()
    name = serializers.CharField()
    cooking_time = serializers.IntegerField()

    class Meta(ShortRecipesSerializer.Meta):
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

    def validate_tags(self, tags):
        self.is_unique(tags, "Теги")
        return tags

    def validate_ingredients(self, ingredients):
        self.is_unique(ingredients, "Ингредиенты")
        for ingredient in ingredients:
            if not BaseIngredients.objects.filter(
                    pk=ingredient.get("id")).exists():
                raise ValidationError(
                    detail={
                        "errors": (
                            "Один или несколько введенных "
                            "Ингредиентов не существуют!"
                        )
                    },
                    code=status.HTTP_400_BAD_REQUEST,
                )
        return ingredients

    def is_unique(self, items, item_name):
        items_id_list = []
        for item in items:
            item_id = item
            if isinstance(item, dict):
                item_id = item.get("id")
            if item_id in items_id_list:
                raise ValidationError(
                    detail={"errors": f"{item_name} должны быть уникальные!"},
                    code=status.HTTP_400_BAD_REQUEST,
                )
            items_id_list.append(item_id)

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
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
            ingredient_obj, _ = Ingredients.objects.get_or_create(
                ingredients=BaseIngredients.objects.get(
                    pk=ingredient.get("id")
                ),
                to_recipe=recipe,
            )
            ingredient_obj.amount = amount
            ingredient_obj.save()
            ingredients_as_object.append(ingredient_obj)
        for ingredient in exist_ingredients:
            if ingredient not in ingredients_as_object:
                ingredient.delete()
        return ingredients_as_object

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance, context=self.context)
        return serializer.data