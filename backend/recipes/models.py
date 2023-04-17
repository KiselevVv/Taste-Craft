from django.db import models
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(
        max_length=settings.RECIPE_LENGTH,
        unique=True,
        # validators=
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=settings.HEX_LENGTH,
        unique=True,
        # validators=
        verbose_name='Цвет в HEX'
    )
    slug = models.CharField(
        max_length=settings.RECIPE_LENGTH,
        unique=True,
        # validators=
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=settings.RECIPE_LENGTH,
        unique=True,
        verbose_name='Ингридиент',
    )
    measurement_unit = models.CharField(
        max_length=settings.MEASUREMENT_LENGTH,
        unique=True,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name, {self.measurement_unit}
