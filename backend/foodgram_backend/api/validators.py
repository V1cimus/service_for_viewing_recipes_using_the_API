from rest_framework import status
from rest_framework.serializers import ValidationError


def validate_subscription(request, model_object, subscribed_object):
    """
    Проверяет подписку пользователя на объект.
    """

    name_model = model_object.model.__name__

    if request.method == "POST":
        if model_object.exists():
            raise ValidationError(
                detail={
                    "errors": f"{subscribed_object} уже"
                    f" добавлен в {name_model}!"
                },
                code=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "subscriber": request.user,
            "subscribed_recipe": subscribed_object,
        }
        return data
    elif request.method == "DELETE":
        if not model_object.exists():
            raise ValidationError(
                detail={"errors": f"{subscribed_object}"
                        f" не добавлен в {name_model}!"},
                code=status.HTTP_404_NOT_FOUND,
            )
        return model_object


def is_unique(items, item_name):
    """
    Проверяет уникальность введенных данных.
    """

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
