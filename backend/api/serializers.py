import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import User, Subscription
from recipes.models import Tag, Ingredient, RecipeIngredient, Recipe


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователей, с дополнительным полем is_subscribed."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and obj.subscribed_to.filter(subscriber=user).exists())


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'password')


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Subscription."""
    class Meta:
        model = Subscription
        fields = ('subscriber', 'subscribed_to')
        read_only_fields = ('subscriber', 'subscribed_to')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели RecipeIngredient."""
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('amount', 'name', 'measurement_unit', 'id')


class Base64ImageField(serializers.ImageField):
    """Поле для загрузки изображений в формате Base64."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class UserRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Recipe, используемый в контексте пользователя.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка рецептов."""
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.BooleanField()
    is_in_shopping_cart = serializers.BooleanField()
    image = Base64ImageField()

    def get_ingredients(self, obj):
        """Возвращает отдельный сериализатор."""
        return RecipeIngredientSerializer(
            RecipeIngredient.objects.filter(recipe=obj).all(), many=True
        ).data

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')


class IngredientCreateInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов в рецепте."""
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(
        write_only=True,
        min_value=1,
        max_value=100000
    )

    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления рецепта."""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientCreateInRecipeSerializer(many=True)
    image = Base64ImageField(required=True)

    def validate_ingredients(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(
                "Добавьте хотя бы один ингредиент.")
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        create_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        RecipeIngredient.objects.bulk_create(
            create_ingredients
        )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients', None)
        if tags:
            instance.tags.clear()
            instance.tags.set(tags)
        if ingredients is not None:
            instance.ingredients.clear()

            create_ingredients = [
                RecipeIngredient(
                    recipe=instance,
                    ingredient=ingredient['ingredient'],
                    amount=ingredient['amount']
                )
                for ingredient in ingredients
            ]
            RecipeIngredient.objects.bulk_create(
                create_ingredients
            )
        return super().update(instance, validated_data)

    def to_representation(self, obj):
        self.fields.pop('ingredients')
        representation = super().to_representation(obj)
        representation['ingredients'] = RecipeIngredientSerializer(
            RecipeIngredient.objects.filter(recipe=obj).all(), many=True
        ).data
        return representation

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')


class UserSubscribeSerializer(UserSerializer):
    """
    Сериализатор для пользователей, отображающий их подписки и количество
    рецептов.
    """
    recipes = UserRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes',
                  'recipes_count')
        read_only_fields = '__all__',

    def get_is_subscribed(*args):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()
