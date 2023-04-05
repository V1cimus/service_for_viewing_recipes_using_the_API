from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.http import HttpResponse
from django.conf import settings


SIZE_TITLE = 24
SIZE_TEXT = 20
SIZE_FOOTER = 14


def start_download_shopping_cart(ingredients_list=None):
    """
    Функция start_download_shopping_cart генерирует PDF-файл
    со списком покупок на основе переданного списка ингредиентов,
    сохраняет его в директории media и возвращает HTTP-ответ с
    этим файлом во вложении.
    """
    data = [[]]
    path_to_pdf = f"{settings.MEDIA_ROOT}/shopping_cart.pdf"
    for ingredient in ingredients_list:
        name = str(ingredient.get("name"))
        amount = str(ingredient.get("total_amount"))
        unit = str(ingredient.get("measurement_unit"))
        data.append([name.lower(), amount.lower(), unit.lower()])
    pdf = canvas.Canvas(path_to_pdf)
    pdfmetrics.registerFont(
        TTFont("my_font", f"{settings.BASE_DIR}/data/font.ttf")
    )
    pdf.setFont("my_font", SIZE_TITLE)
    pdf.setTitle("Список покупок!")
    table = Table(data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                ("ALIGN", (0, 1), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 1), (-1, -1), "my_font"),
                ("FONTSIZE", (0, 1), (-1, -1), SIZE_TEXT),
            ]
        )
    )
    y_table = 750 - (len(data) - 1) * SIZE_TEXT
    table.wrapOn(pdf, 0, 0)
    table.drawOn(pdf, 100, y_table)
    pdf.drawString(200, 770, "Список покупок!")
    pdf.setFont("my_font", SIZE_FOOTER)
    pdf.drawString(
        250,
        y_table - SIZE_TEXT * 2,
        "Список покупок создан при помощи FoodGram в "
        f"{datetime.now().strftime('%H:%M:%S')}",
    )
    pdf.save()
    with open(path_to_pdf, "rb") as file:
        response = HttpResponse(
            file, content_type="application/pdf"
        )
        response["Content-Disposition"] = (
            "attachment; filename=shopping_list.pdf"
        )
    return response
