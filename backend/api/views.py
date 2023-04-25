from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from recipes.models import Tag, Ingredient, Recipe, Favorite, Cart
from .filters import TagFilter
from .permissions import IsAdminOrReadOnly
from .serializers import (SubscriptionSerializer, TagSerializer,
                          IngredientSerializer, RecipeCreateUpdateSerializer,
                          RecipeListSerializer, UserSubscribeSerializer,
                          UserRecipeSerializer)
from users.models import User, Subscription


class SubscriptionsListViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = User.objects.filter(subscribed_to__subscriber=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = UserSubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class SubscribeViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, user_id=None):
        subscriber = request.user
        subscribed_to = get_object_or_404(User, pk=user_id)
        if subscriber == subscribed_to:
            return Response(
                {'errors': 'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset = Subscription.objects.create(
            subscribed_to=subscribed_to,
            subscriber=subscriber
        )
        serializer = SubscriptionSerializer(
            queryset,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id=None):
        subscribed_to = get_object_or_404(User, pk=user_id)
        get_object_or_404(Subscription, subscriber=request.user,
                          subscribed_to=subscribed_to).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = TagFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateUpdateSerializer
        return RecipeListSerializer

    def get_queryset(self):
        qs = Recipe.objects.add_user_annotations(self.request.user.pk)
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        author = self.request.query_params.get('author', None)
        if is_favorited:
            qs = qs.filter(favorites__user=self.request.user)
        if is_in_shopping_cart:
            qs = qs.filter(cart__user=self.request.user)
        if author:
            qs = qs.filter(author=author)
        return qs

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = UserRecipeSerializer(recipe, data=request.data,
                                              context={"request": request})
            serializer.is_valid(raise_exception=True)
            if not Favorite.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                Favorite.objects.create(user=request.user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(Favorite, user=request.user,
                              recipe=recipe).delete()
            return Response({'detail': 'Рецепт удален из избранного.'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = UserRecipeSerializer(recipe, data=request.data,
                                              context={"request": request})
            serializer.is_valid(raise_exception=True)
            if not Cart.objects.filter(user=request.user,
                                       recipe=recipe).exists():
                Cart.objects.create(user=request.user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(Cart, user=request.user,
                              recipe=recipe).delete()
            return Response(
                {'detail': 'Рецепт удален из списка покупок.'},
                status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = Cart.objects.filter(
            user=request.user.id).values_list(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit'
        ).annotate(ingredient_amount=Sum('recipe__recipeingredient__amount'))

        response = HttpResponse(content_type='text/plain')
        response[
            'Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'

        for item in ingredients:
            response.write(
                f"* {item[0]} ({item[1]}) — {item[2]}\n"
            )

        return response
