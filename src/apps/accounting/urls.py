from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.accounting.api.viewsets.finances import TradingPairViewSet

app_name = 'accounting'

router = DefaultRouter()
router.register(r'trading-pairs', TradingPairViewSet, basename='trading-pair')

urlpatterns = [
    path('', include(router.urls), name='trading-pair'),
]
