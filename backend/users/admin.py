from django.conf import settings
from django.contrib import admin

from .models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    empty_value_display = '-пусто-'
    list_filter = ('is_active',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('pk', 'username', 'email')


@admin.register(Subscription)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subscriber', 'subscribed_to')
    list_editable = ('subscriber', 'subscribed_to')
    empty_value_display = '-пусто-'
