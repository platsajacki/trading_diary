import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounting.api.serializers.finances import TradingPairSerializer
from apps.accounting.models.finances import TradingPair


@pytest.mark.usefixtures('bybit_futures_trading_pairs', 'bybit_spot_trading_pairs')
class TestTradingPairViewSet:
    url_list = reverse('api:v1:accounting:trading-pair-list')
    url_retrieve = reverse('api:v1:accounting:trading-pair-detail', args=[1])

    def test_list_anonymous_user(self, client: APIClient):
        response = client.get(self.url_list)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_authenticated_user(self, api_client: APIClient):
        response = api_client.get(self.url_list)
        assert response.status_code == status.HTTP_200_OK
        qs = TradingPair.objects.with_select_related()
        assert response.data == TradingPairSerializer(qs, many=True).data

    def test_list_authenticated_user_with_filter(
        self, api_client: APIClient, bybit_futures_trading_pairs: list[TradingPair]
    ):
        ticker = bybit_futures_trading_pairs[0].base_asset.ticker
        response = api_client.get(self.url_list, {'base_asset__ticker': ticker})
        assert response.status_code == status.HTTP_200_OK
        qs = TradingPair.objects.with_select_related().filter(base_asset__ticker=ticker)
        assert response.data == TradingPairSerializer(qs, many=True).data

    def test_retrieve_anonymous_user(self, client: APIClient):
        response = client.get(self.url_retrieve)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_authenticated_user(self, api_client: APIClient):
        response = api_client.get(self.url_retrieve)
        assert response.status_code == status.HTTP_200_OK
        qs = TradingPair.objects.with_select_related().get(pk=1)
        assert response.data == TradingPairSerializer(qs).data
