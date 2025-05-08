from django.urls import path

from accounting.api.viewsets.finances import TradingPairListAPIView

urlpatterns = [
    path('trading-pairs/', TradingPairListAPIView.as_view(), name='trading-pair'),
]
