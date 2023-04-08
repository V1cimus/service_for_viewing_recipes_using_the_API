from csv import DictReader

from django.core.management import BaseCommand
from tqdm import tqdm

from recipes.models import BaseIngredient


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open("data/ingredients.csv", encoding="utf-8") as file:
            rows = list(DictReader(file))
        for row in tqdm(rows, desc="Upload ingredients", colour="green"):
            name = row.get("name")
            BaseIngredient.objects.get_or_create(
                    name=name,
                    measurement_unit=row.get("measurement_unit"),
                )
