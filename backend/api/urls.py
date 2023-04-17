from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SubscriptionsListViewSet, SubscribeViewSet, TagViewSet, \
    IngredientViewSet

app_name = 'api'

router = SimpleRouter()
router.register('users/subscriptions', SubscriptionsListViewSet,
                basename='subscriptions')
router.register(r'users/(?P<user_id>\d+)/subscribe', SubscribeViewSet,
                basename='subscribe')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
