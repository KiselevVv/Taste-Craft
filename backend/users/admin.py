from django.conf import settings
from django.contrib import admin

from .models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Административная панель для модели User.

    Список отображаемых полей:
    - 'pk': Идентификатор пользователя.
    - 'username': Имя пользователя.
    - 'email': Адрес электронной почты пользователя.
    - 'first_name': Имя пользователя.
    - 'last_name': Фамилия пользователя.
    """
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
    """
    Административная панель для модели Subscription.

    Список отображаемых полей:
    - 'pk': Идентификатор подписки.
    - 'subscriber': Подписчик.
    - 'subscribed_to': Пользователь, на которого подписан подписчик.
    """
    list_display = ('pk', 'subscriber', 'subscribed_to')
    list_editable = ('subscriber', 'subscribed_to')
    empty_value_display = '-пусто-'
