import io
from datetime import datetime

from django.conf import settings
from django.http import FileResponse
from reportlab.lib.colors import black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

START_X_COORD = 0
START_Y_COORD = 0
COORD_FIRST_CELL = (0, 0)
COORD_LAST_CELL = (-1, -1)
COORD_X_TITLE = 200
COORD_Y_TITLE = 770
COORD_X_TABLE = 100
COORD_X_FOOTER = 250
SIZE_TITLE = 24
SIZE_TEXT = 20
SIZE_FOOTER = 14


def create_data_for_table(ingredients_list=None):
    """
    Функция преобразует список ингредиентов в список
    списков для дальнейшего использования в создании таблицы.

    Возвращает:
    data - данные с названием ингредиента,
    его количеством и единицей измерения.
    """
    data = []
    for ingredient in ingredients_list:
        name = str(ingredient.get("name"))
        amount = str(ingredient.get("total_amount"))
        unit = str(ingredient.get("measurement_unit"))
        data.append([name.lower(), amount.lower(), unit.lower()])
    return data


def create_table(pdf, data=None):
    """
    Функция создает таблицу в PDF-документе.

    Возвращает:
    bottom_coord_table - координаты
    нижнего левого угла таблицы.
    """
    table = Table(data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", COORD_FIRST_CELL, COORD_LAST_CELL, white),
                ("TEXTCOLOR", COORD_FIRST_CELL, COORD_LAST_CELL, black),
                ("ALIGN", COORD_FIRST_CELL, COORD_LAST_CELL, "LEFT"),
                ("FONTNAME", COORD_FIRST_CELL, COORD_LAST_CELL, "my_font"),
                ("FONTSIZE", COORD_FIRST_CELL, COORD_LAST_CELL, SIZE_TEXT),
            ]
        )
    )
    y_table = COORD_Y_TITLE - (len(data) + 1) * SIZE_TEXT
    table.wrapOn(pdf, START_X_COORD, START_Y_COORD)
    table.drawOn(pdf, COORD_X_TABLE, y_table)
    bottom_coord_table = (COORD_X_TABLE, y_table)
    return bottom_coord_table


def start_download_shopping_cart(ingredients_list=None):
    """
    Функция start_download_shopping_cart генерирует PDF-файл
    со списком покупок на основе переданного списка ингредиентов,
    сохраняет его в буфер и возвращает HTTP-ответ с
    файлом во вложении.
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont(
        "my_font", f"{settings.BASE_DIR}/data/font.ttf")
    )
    pdf.setFont("my_font", SIZE_TITLE)
    pdf.setTitle("Список покупок!")
    pdf.drawString(COORD_X_TITLE, COORD_Y_TITLE, "Список покупок!")
    _, y_table = create_table(pdf, create_data_for_table(ingredients_list))
    pdf.setFont("my_font", SIZE_FOOTER)
    pdf.drawString(
        COORD_X_FOOTER,
        y_table - SIZE_TEXT * 2,
        "Список покупок создан при помощи FoodGram в "
        f"{datetime.now().strftime('%H:%M:%S')}",
    )
    pdf.save()
    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True, filename='shopping_list.pdf'
    )
