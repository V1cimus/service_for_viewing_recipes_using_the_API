from django.contrib import admin

from .models import User, SubscribAuthor


@admin.register(User)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
    search_fields = ("username", "email",)
    list_filter = ("username", "email",)
    empty_value_display = "---пусто---"


admin.site.register(SubscribAuthor)
