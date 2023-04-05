from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator
from colorfield.fields import ColorField


User = get_user_model()


class Unit(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name="Единица измерения",
    )

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"
        ordering = ("name",)

    def __str__(self):
        return self.name


class BaseIngredients(models.Model):
    name = models.CharField(
        unique=True,
        max_length=64,
        verbose_name="Название продукта",
    )
    measurement_unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name="Единица измерения",
    )

    class Meta:
        verbose_name = "Название продукта"
        verbose_name_plural = "Название продуктов"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    ingredients = models.ForeignKey(
        BaseIngredients,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="Название продукта",
    )
    amount = models.IntegerField(
        verbose_name="Количество продукта",
        validators=[
            MinValueValidator(1),
        ],
        null=True,
    )
    to_recipe = models.ForeignKey(
        "Recipe",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="ingredient_to_recipe",
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("ingredients",)

    def __str__(self):
        return f"{self.ingredients.name} - {self.amount}"


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=32,
        verbose_name="Название тега",
    )
    slug = models.SlugField(unique=True, verbose_name="Ссылка на тег")
    color = ColorField(
        unique=True,
        verbose_name="Цвет тега",
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="author_recipe",
        verbose_name="Автор",
    )
    name = models.CharField(
        max_length=32,
        verbose_name="Название рецепта",
    )
    image = models.ImageField(
        upload_to="recipes/image/",
        null=True,
        default=None,
        verbose_name="Изображение рецепта",
    )
    text = models.TextField(
        max_length=256,
        verbose_name="Описание рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        verbose_name="Ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Тег",
        related_name="tags",
    )
    cooking_time = models.IntegerField(
        verbose_name="Время приготовления в минутах",
        validators=[
            MinValueValidator(1),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name="дата публикации", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class BaseAddRecipe(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="%(class)s_subscriber",
    )
    subscribed_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="%(class)s_subscribed_recipe",
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=("subscriber", "subscribed_recipe"),
                name="unique appversion %(class)s",
            )
        ]

    def __str__(self):
        return f"{self.subscriber} -> {self.subscribed_recipe}"


class Favorite(BaseAddRecipe):
    class Meta(BaseAddRecipe.Meta):
        verbose_name = "Подписка на рецепт"
        verbose_name_plural = "Подписки на рецепты"


class ShoppingList(BaseAddRecipe):
    class Meta(BaseAddRecipe.Meta):
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
