from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.accounting.api.viewsets.finances import TradingPairViewSet
from apps.accounting.api.viewsets.positions import PositionViewSet

app_name = 'accounting'

router = DefaultRouter()
router.register(r'trading-pairs', TradingPairViewSet, basename='trading-pair')
router.register(r'positions', PositionViewSet, basename='position')

urlpatterns = [
    path('', include(router.urls), name='trading-pair'),
]
