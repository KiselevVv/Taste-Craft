from django.contrib import admin

from recipes.models import Tag, Ingredient

admin.site.register(Tag)
admin.site.register(Ingredient)
