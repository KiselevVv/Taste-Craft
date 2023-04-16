from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SubscriptionsListViewSet, SubscribeViewSet

app_name = 'api'

router = SimpleRouter()
router.register('users/subscriptions', SubscriptionsListViewSet,
                basename='subscriptions')
router.register(r'users/(?P<user_id>\d+)/subscribe', SubscribeViewSet,
                basename='subscribe')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
