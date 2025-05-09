from django.urls import path

from apps.accounting.api.viewsets.finances import TradingPairListAPIView

app_name = 'accounting'

urlpatterns = [
    path('trading-pairs/', TradingPairListAPIView.as_view(), name='trading-pair-list'),
]
