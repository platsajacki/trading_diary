from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.accounting.api.viewsets.finances import TradingPairListAPIView

app_name = 'accounting'

router = DefaultRouter()
router.register(r'trading-pairs', TradingPairListAPIView, basename='trading-pair')

urlpatterns = [
    path('', include(router.urls), name='trading-pair'),
]
