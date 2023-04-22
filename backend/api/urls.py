from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import (SubscriptionsListViewSet, SubscribeViewSet, TagViewSet,
                    IngredientViewSet, RecipesViewSet)

app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register('users/subscriptions', SubscriptionsListViewSet,
                   basename='subscriptions')
router_v1.register(r'users/(?P<user_id>\d+)/subscribe', SubscribeViewSet,
                   basename='subscribe')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
