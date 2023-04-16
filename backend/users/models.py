from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    """Класс для переопределения модели пользователя."""

    username = models.CharField(
        max_length=settings.NAME_PASS_LENGTH,
        unique=True,
        validators=[validate_username],
        verbose_name='Юзернейм'
    )
    password = models.CharField(
        max_length=settings.NAME_PASS_LENGTH,
        verbose_name='Пароль'
    )
    email = models.EmailField(
        max_length=settings.EMAIL_LENGTH,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(
        max_length=settings.NAME_PASS_LENGTH,
        blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=settings.NAME_PASS_LENGTH,
        blank=False,
        verbose_name='Фамилия'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    subscribed_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed_to',
        verbose_name='Подписан на'
    )

    def __str__(self):
        return f'{self.subscriber.username} -> {self.subscribed_to.username}'

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'subscribed_to'],
                name='unique_subscribe'
            )
        ]
