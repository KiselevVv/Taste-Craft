from djoser.serializers import UserCreateSerializer, UserSerializer

from rest_framework import serializers

from users.models import User, Subscription


class CustomUserSerializer(UserSerializer):
    """Cписок пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated and
                obj.subscribed_to.filter(subscriber=user).exists())


class CustomUserCreateSerializer(UserCreateSerializer):
    """Создание нового пользователя."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'password')


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('subscriber', 'subscribed_to')
        read_only_fields = ('subscriber', 'subscribed_to')
