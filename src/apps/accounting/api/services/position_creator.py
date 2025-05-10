from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.accounting.api.serializers.positions import PositionReadSerializer
from apps.accounting.models import Position
from apps.accounting.models.finances import TradingPair
from apps.core.services.interfaces import ViewSetService


class PositionCreator(ViewSetService):
    def get_trading_pair(self, data: dict) -> TradingPair:
        symbol = data.pop('symbol')
        market = data.pop('market')
        exchange = data.pop('exchange')
        trading_pair = TradingPair.objects.get_by_symbol(
            symbol=symbol,
            market=market,
            exchange=exchange,
        )
        if not trading_pair:
            raise NotFound(f'Trading pair with symbol {symbol} not found in {market} on {exchange}.')
        return trading_pair

    def act(self) -> Response:
        data = self.get_validated_data()
        data['user'] = self.request.user
        data['trading_pair'] = self.get_trading_pair(data)
        position = Position.objects.create(**data)
        serializer_data = PositionReadSerializer(position).data
        headers = self.viewset.get_success_headers(serializer_data)
        return Response(serializer_data, status=status.HTTP_201_CREATED, headers=headers)
