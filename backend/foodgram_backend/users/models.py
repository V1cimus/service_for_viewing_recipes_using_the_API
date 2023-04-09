from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        verbose_name=_("Name"),
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name=_("Last Name"),
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )
    is_user_ban = models.BooleanField(
        default=False,
        verbose_name=_("Ban"),
    )

    class Meta:
        ordering = ("id",)
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username

    @property
    def is_ban(self):
        return self.is_user_ban

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriber",
        verbose_name=_("User"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribing",
        verbose_name=_("Author"),
    )

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        constraints = [
            models.UniqueConstraint(
                fields=("user", "author"), name="unique_subscribe"
            )
        ]
        indexes = (
            models.Index(fields=('user', 'author',)),
        )

    def __str__(self):
        return f"{self.user} -> {self.author}"
