# Generated by Django 4.1.7 on 2023-04-08 06:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0007_alter_ingredient_amount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="amount",
            field=models.IntegerField(
                default=1,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Количество продукта",
            ),
        ),
    ]
