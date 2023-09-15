from django.contrib import admin

from .models import (Tag, Ingredient, Recipe, RecipeIngredient,
                     Favorite, Cart)

admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Cart)


class IngredientTabular(admin.TabularInline):
    """Инлайн-форма для ингредиентов в административной панели рецептов."""
    model = RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Recipe.

    Список отображаемых полей:
    - 'pk': Идентификатор рецепта.
    - 'author': Автор рецепта.
    - 'name': Название рецепта.
    - 'pub_date': Дата публикации рецепта.
    - 'count_favorites': Количество избранных рецептов.
    """
    list_display = (
        'pk',
        'author',
        'name',
        'pub_date',
        'count_favorites'
    )
    search_fields = ('name', 'author', 'tags')
    inlines = [
        IngredientTabular,
    ]

    def count_favorites(self, obj):
        return obj.favorites.count()

    count_favorites.short_description = 'в избранном (кол-во)'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Административная панель для модели Ingredient."""
    search_fields = ('name',)
