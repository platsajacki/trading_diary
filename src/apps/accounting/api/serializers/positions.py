from rest_framework import serializers

from apps.accounting.api.serializers.finances import TradingPairSerializer
from apps.accounting.models import Position, PositionComment
from apps.accounting.models.enums import Exchange, MarketType


class PositionCommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев к позиции."""

    class Meta:
        model = PositionComment
        fields = [
            'id',
            'position',
            'comment',
            'chart_link',
            'created_at',
            'modified_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'modified_at',
        ]
        write_only_fields = [
            'position',
        ]


class PositionCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания позиции."""

    symbol = serializers.CharField()
    market = serializers.ChoiceField(choices=MarketType.choices)
    exchange = serializers.ChoiceField(choices=Exchange.choices)

    class Meta:
        model = Position
        fields = [
            'symbol',
            'market',
            'exchange',
            'is_closed',
            'side',
            'size',
            'entry_price',
            'leverage',
            'liq_price',
            'take_profit',
            'stop_loss',
            'trailing_stop',
            'type_trailing_stop',
            'opened_at',
            'closed_at',
        ]


class PositionReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения позиции."""

    trading_pair = TradingPairSerializer(read_only=True)
    symbol = serializers.CharField(source='trading_pair.symbol')
    market = serializers.CharField(source='trading_pair.base_asset.market')
    exchange = serializers.CharField(source='trading_pair.base_asset.exchange')
    comments = PositionCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Position
        fields = [
            'id',
            'symbol',
            'market',
            'exchange',
            'user',
            'trading_pair',
            'is_closed',
            'side',
            'size',
            'position_value',
            'entry_price',
            'leverage',
            'liq_price',
            'take_profit',
            'stop_loss',
            'trailing_stop',
            'type_trailing_stop',
            'opened_at',
            'closed_at',
            'created_at',
            'modified_at',
            'comments',
        ]
        read_only_fields = fields


class PositionUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления позиции."""

    class Meta:
        model = Position
        fields = [
            'is_closed',
            'side',
            'size',
            'entry_price',
            'leverage',
            'liq_price',
            'take_profit',
            'stop_loss',
            'trailing_stop',
            'type_trailing_stop',
            'opened_at',
            'closed_at',
        ]
        write_only_fields = fields
