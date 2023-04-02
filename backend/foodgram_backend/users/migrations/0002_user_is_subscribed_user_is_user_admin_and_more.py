# Generated by Django 4.1.7 on 2023-03-26 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_subscribed',
            field=models.BooleanField(default=False, verbose_name='Подписан'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_user_admin',
            field=models.BooleanField(default=False, verbose_name='Администратор'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_user_ban',
            field=models.BooleanField(default=False, verbose_name='Заблокировать'),
        ),
        migrations.CreateModel(
            name='SubscribAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribing', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.AddConstraint(
            model_name='subscribauthor',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique appversion'),
        ),
    ]
