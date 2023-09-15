from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Exists, OuterRef
from recipes.validators import validate_color
from users.models import User


class Tag(models.Model):
    """
    Модель для тегов рецептов.

    Поля:
    - name (CharField): Название тега.
    - color (CharField): Цвет тега в формате HEX.
    - slug (CharField): Уникальный слаг тега.
    """
    name = models.CharField(
        max_length=settings.RECIPE_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=settings.HEX_LENGTH,
        unique=True,
        validators=[validate_color],
        verbose_name='Цвет в HEX'
    )
    slug = models.CharField(
        max_length=settings.RECIPE_LENGTH,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель для ингредиентов.

    Поля:
    - name (CharField): Название ингредиента.
    - measurement_unit (CharField): Единица измерения для ингредиента.
    """
    name = models.CharField(
        max_length=settings.RECIPE_LENGTH,
        unique=True,
        verbose_name='Ингридиент',
    )
    measurement_unit = models.CharField(
        max_length=settings.MEASUREMENT_LENGTH,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredients'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class RecipeQuerySet(models.QuerySet):
    """
     Менеджер запросов для модели Recipe.
    """
    def add_user_annotations(self, user_id):
        return self.annotate(
            is_favorited=Exists(
                Favorite.objects.filter(
                    user_id=user_id, recipe__pk=OuterRef('pk')
                )
            ),
            is_in_shopping_cart=Exists(
                Cart.objects.filter(
                    user_id=user_id, recipe__pk=OuterRef('pk')
                )
            ),
        )


class Recipe(models.Model):
    """
    Модель для рецептов.

    Поля:
    - tags (ManyToManyField): Теги, связанные с рецептом.
    - author (ForeignKey): Автор рецепта.
    - ingredients (ManyToManyField): Ингредиенты, связанные с рецептом.
    - name (CharField): Название рецепта.
    - image (ImageField): Картинка рецепта.
    - text (TextField): Текст рецепта.
    - cooking_time (PositiveSmallIntegerField): Время приготовления рецепта.
    - pub_date (DateTimeField): Дата публикации рецепта.
    """
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэг'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты'
    )
    name = models.CharField(
        max_length=settings.RECIPE_LENGTH,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
        verbose_name='Картинка'
    )
    text = models.TextField(verbose_name='Текст')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        default=settings.COOKING_TIME
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """
    Модель для ингредиентов в рецептах.

    Поля:
    - amount (PositiveIntegerField): Количество ингредиента в рецепте.
    - ingredient (ForeignKey): Ингредиент.
    - recipe (ForeignKey): Рецепт.
    """
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[
            MaxValueValidator(100000),
            MinValueValidator(1)
        ]
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'


class Favorite(models.Model):
    """
    Модель для избранных рецептов пользователей.

    Поля:
    - user (ForeignKey): Пользователь.
    - recipe (ForeignKey): Рецепт.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_user_recipe'
            )
        ]
        verbose_name = 'Рецеп из избранного'
        verbose_name_plural = 'Рецепты из избранного'


class Cart(models.Model):
    """
    Модель для списка покупок пользователей.

    Поля:
    - user (ForeignKey): Пользователь.
    - recipe (ForeignKey): Рецепт.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Список покупок'
    )

    def __str__(self):
        return f'{self.recipe} в списке покупок у {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_cart_user_recipes'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
