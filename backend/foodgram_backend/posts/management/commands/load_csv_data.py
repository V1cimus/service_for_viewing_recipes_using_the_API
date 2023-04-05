from csv import DictReader

from django.core.management import BaseCommand
from posts.models import BaseIngredients, Unit


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for row in DictReader(
                open("data/ingredients.csv", encoding="utf-8")
                ):
            unit, status = Unit.objects.get_or_create(
                    name=row.get("measurement_unit")
                )
            name = row.get("name")
            if status:
                baseingredients = BaseIngredients(
                    name=name, measurement_unit=unit
                )
                baseingredients.save()
            else:
                print(f"baseingredient <{name}> уже существует!")