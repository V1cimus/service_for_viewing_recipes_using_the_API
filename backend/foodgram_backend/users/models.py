from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        null=False,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        null=False,
        verbose_name='Фамилия',
    )
    email = models.EmailField(
        unique=True,
        null=False,
        verbose_name="Email",
    )
    is_user_ban = models.BooleanField(
        default=False, verbose_name="Заблокировать",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    @property
    def is_ban(self):
        return self.is_user_ban


class SubscribAuthor(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'), name='unique_subscrib'
            )
        ]

    def __str__(self):
        return f'{self.user} -> {self.author}'
