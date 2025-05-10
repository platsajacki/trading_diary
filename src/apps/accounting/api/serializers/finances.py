from collections import defaultdict

from rest_framework import serializers

from apps.accounting.managers.finances import TradingPairQuerySet
from apps.accounting.models import FinancialAsset, TradingPair


class FinancialAssetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели FinancialAsset.

    Поля:
        ticker (str): Тикер актива, уникальный идентификатор.
        type (str): Тип актива, например, акция, валюта или криптовалюта.
        market (str): Рынок, на котором торгуется актив, например, спот или фьючерсы.
        exchange (str): Биржа, на которой зарегистрирован актив.
    """

    class Meta:
        model = FinancialAsset
        fields = [
            'ticker',
            'type',
            'market',
            'exchange',
            'created_at',
            'modified_at',
        ]
        read_only_fields = fields


class TradingPairListSerializer(serializers.ListSerializer):
    """
    Сериализатор для списка торговых пар.
    Группирует торговые пары по биржам и сериализует их.
    """

    def to_representation(self, data: TradingPairQuerySet | None) -> defaultdict:  # type: ignore[override]
        exchanges: defaultdict = defaultdict(lambda: defaultdict(list))
        if data is None:
            return exchanges
        for pair in data:
            if self.child is None:
                raise ValueError('Child serializer is not set.')
            serialized_pair = self.child.to_representation(pair)
            exchanges[pair.base_asset.exchange][pair.base_asset.market].append(serialized_pair)
        return exchanges

    @property
    def data(self) -> dict:  # type: ignore[override]
        return self.to_representation(self.instance)


class TradingPairSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели TradingPair.
    Поля:
        base_asset (FinancialAsset): Базовый актив в паре.
        quote_asset (FinancialAsset): Котируемый актив в паре.
        traded (bool): Флаг, указывающий, торгуется ли пара.
        created_at (datetime): Дата и время создания пары.
        modified_at (datetime): Дата и время последнего изменения пары.
    """

    base_asset = FinancialAssetSerializer()
    quote_asset = FinancialAssetSerializer()

    class Meta:
        model = TradingPair
        list_serializer_class = TradingPairListSerializer
        fields = [
            'symbol',
            'base_asset',
            'quote_asset',
            'traded',
            'created_at',
            'modified_at',
        ]
        read_only_fields = fields
        ref_name = 'TradingPair'
