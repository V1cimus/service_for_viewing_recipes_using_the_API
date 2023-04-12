from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class BaseIngredient(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_("Product Name"),
    )
    measurement_unit = models.CharField(
        max_length=32,
        verbose_name=_("Measurement Unit"),
    )

    class Meta:
        verbose_name = _("Product Name")
        verbose_name_plural = _("Products Name")
        ordering = ("name",)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    ingredient = models.ForeignKey(
        BaseIngredient,
        on_delete=models.CASCADE,
        related_name="ingredient",
        verbose_name=_("Product Name"),
    )
    amount = models.IntegerField(
        verbose_name=_("Quantity of Product"),
        validators=(
            MinValueValidator(1),
        ),
    )
    to_recipe = models.ForeignKey(
        "Recipe",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="ingredient_to_recipe",
        verbose_name=_("Recipe"),
    )

    class Meta:
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")
        ordering = ("ingredient",)
        indexes = (
            models.Index(fields=('ingredient',)),
        )

    def __str__(self):
        return f"{self.ingredient.name} - {self.amount}"


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=32,
        verbose_name=_("Tag Name"),
    )
    slug = models.SlugField(unique=True, verbose_name=_("Tag Slug"))
    color = ColorField(
        unique=True,
        verbose_name=_("Tag Color"),
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ("name",)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="author_recipe",
        verbose_name=_("Author"),
    )
    name = models.CharField(
        max_length=32,
        verbose_name=_("Recipe Name"),
    )
    image = models.ImageField(
        upload_to="recipes/image/",
        null=True,
        default=None,
        verbose_name=_("Recipe image"),
    )
    text = models.TextField(
        max_length=2048,
        verbose_name=_("Recipe Discription"),
    )
    ingredients = models.ManyToManyField(
        BaseIngredient,
        through="Ingredient",
        verbose_name=_("Ingredients"),
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("Tags"),
        related_name="tags",
    )
    cooking_time = models.IntegerField(
        verbose_name=_("Cooking Time in Minutes"),
        validators=[
            MinValueValidator(1),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name=_("Publication Date"), auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="favorite_subscriber",
    )
    subscribed_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_("Recipe"),
        related_name="favorite_subscribed_recipe",
    )

    class Meta:
        verbose_name = _("Favorite Recipe")
        verbose_name_plural = _("Favorite Recipes")
        constraints = [
            models.UniqueConstraint(
                fields=("subscriber", "subscribed_recipe"),
                name="unique appversion favorite",
            )
        ]
        indexes = (
            models.Index(fields=('subscriber', 'subscribed_recipe',)),
        )

    def __str__(self):
        return f"{self.subscriber} -> {self.subscribed_recipe}"


class ShoppingList(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="shoppinglist_subscriber",
    )
    subscribed_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_("Recipe"),
        related_name="shoppinglist_subscribed_recipe",
    )

    class Meta:
        verbose_name = _("Shopping List")
        verbose_name_plural = _("Shopping Lists")
        constraints = [
            models.UniqueConstraint(
                fields=("subscriber", "subscribed_recipe"),
                name="unique appversion shoppinglist",
            )
        ]
        indexes = (
            models.Index(fields=('subscriber', 'subscribed_recipe',)),
        )

    def __str__(self):
        return f"{self.subscriber} -> {self.subscribed_recipe}"
