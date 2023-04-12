# Generated by Django 4.1.7 on 2023-04-12 13:07

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseIngredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=64, unique=True, verbose_name="Product Name"
                    ),
                ),
                (
                    "measurement_unit",
                    models.CharField(max_length=32, verbose_name="Measurement Unit"),
                ),
            ],
            options={
                "verbose_name": "Product Name",
                "verbose_name_plural": "Products Name",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Quantity of Product",
                    ),
                ),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredient",
                        to="recipes.baseingredient",
                        verbose_name="Product Name",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ingredient",
                "verbose_name_plural": "Ingredients",
                "ordering": ("ingredient",),
            },
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="Recipe Name")),
                (
                    "image",
                    models.ImageField(
                        default=None,
                        null=True,
                        upload_to="recipes/image/",
                        verbose_name="Recipe image",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        max_length=2048, verbose_name="Recipe Discription"
                    ),
                ),
                (
                    "cooking_time",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Cooking Time in Minutes",
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Publication Date",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author_recipe",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
                (
                    "ingredients",
                    models.ManyToManyField(
                        through="recipes.Ingredient",
                        to="recipes.baseingredient",
                        verbose_name="Ingredients",
                    ),
                ),
            ],
            options={
                "verbose_name": "Recipe",
                "verbose_name_plural": "Recipes",
                "ordering": ("-pub_date",),
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=32, unique=True, verbose_name="Tag Name"
                    ),
                ),
                ("slug", models.SlugField(unique=True, verbose_name="Tag Slug")),
                (
                    "color",
                    colorfield.fields.ColorField(
                        default="#FFFFFF",
                        image_field=None,
                        max_length=18,
                        samples=None,
                        unique=True,
                        verbose_name="Tag Color",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tag",
                "verbose_name_plural": "Tags",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="ShoppingList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subscribed_recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shoppinglist_subscribed_recipe",
                        to="recipes.recipe",
                        verbose_name="Recipe",
                    ),
                ),
                (
                    "subscriber",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shoppinglist_subscriber",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Shopping List",
                "verbose_name_plural": "Shopping Lists",
            },
        ),
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(
                related_name="tags", to="recipes.tag", verbose_name="Tags"
            ),
        ),
        migrations.AddField(
            model_name="ingredient",
            name="to_recipe",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient_to_recipe",
                to="recipes.recipe",
                verbose_name="Recipe",
            ),
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subscribed_recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorite_subscribed_recipe",
                        to="recipes.recipe",
                        verbose_name="Recipe",
                    ),
                ),
                (
                    "subscriber",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorite_subscriber",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Favorite Recipe",
                "verbose_name_plural": "Favorite Recipes",
            },
        ),
        migrations.AddIndex(
            model_name="shoppinglist",
            index=models.Index(
                fields=["subscriber", "subscribed_recipe"],
                name="recipes_sho_subscri_ff6def_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="shoppinglist",
            constraint=models.UniqueConstraint(
                fields=("subscriber", "subscribed_recipe"),
                name="unique appversion shoppinglist",
            ),
        ),
        migrations.AddIndex(
            model_name="ingredient",
            index=models.Index(
                fields=["ingredient"], name="recipes_ing_ingredi_602db0_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="favorite",
            index=models.Index(
                fields=["subscriber", "subscribed_recipe"],
                name="recipes_fav_subscri_6eb5ec_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(
                fields=("subscriber", "subscribed_recipe"),
                name="unique appversion favorite",
            ),
        ),
    ]
