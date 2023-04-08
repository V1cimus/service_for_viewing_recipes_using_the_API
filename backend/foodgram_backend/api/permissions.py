from rest_framework import permissions


class IsNotBanPermission(permissions.BasePermission):
    """
    Проверяет, заблокирован ли пользователь.
    """

    message = "Ваш аккаунт заблокирован :("

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return True
        return not request.user.is_ban


class AuthorPermission(permissions.BasePermission):
    """
    Проверяет, является ли пользователь автором объекта.
    """

    message = "Доступно только автору!"

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """
    Проверяет, имеет ли пользователь права администратора
    или же разрешено только чтение.
    """

    message = (
        "Доступ разрешен только для администратора или только для чтения."
    )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or self.is_admin
        )
