from apps.accounting.models import Position, TradingPair
from apps.core.filtersets import FilterSet


class TradingPairFilterSet(FilterSet):
    """
    Фильтр для модели TradingPair.

    Метод поиска фильтров:
        - Для строковых полей используется два типа фильтров:
            • exact: для точного совпадения значения поля.
            • icontains: для поиска подстроки в значении поля без учета регистра.

    Поля фильтра:
        - base_asset__ticker: Тикер базового актива.
        - quote_asset__ticker: Тикер котируемого актива.
        - base_asset__type: Тип базового актива.
        - quote_asset__type: Тип котируемого актива.
        - base_asset__market: Рынок базового актива.
        - quote_asset__market: Рынок котируемого актива.
        - traded: Флаг, указывающий, торгуется ли пара.
    """

    class Meta:
        model = TradingPair
        fields = {
            'base_asset__ticker': ['exact', 'icontains'],
            'quote_asset__ticker': ['exact', 'icontains'],
            'base_asset__type': ['exact', 'icontains'],
            'quote_asset__type': ['exact', 'icontains'],
            'base_asset__market': ['exact', 'icontains'],
            'quote_asset__market': ['exact', 'icontains'],
            'traded': ['exact'],
        }


class PositionFilterSet(FilterSet):
    """
    Фильтр для модели Position.

    Поля фильтра:
        - trading_pair__base_asset__ticker: Тикер базового актива.
        - trading_pair__quote_asset__ticker: Тикер котируемого актива.
        - trading_pair__base_asset__type: Тип базового актива.
        - trading_pair__quote_asset__type: Тип котируемого актива.
        - trading_pair__base_asset__market: Рынок базового актива.
        - trading_pair__quote_asset__market: Рынок котируемого актива.
        - traded: Флаг, указывающий, торгуется ли пара.
    """

    class Meta:
        model = Position
        fields = {
            'trading_pair__base_asset__ticker': ['exact', 'icontains'],
            'trading_pair__quote_asset__ticker': ['exact', 'icontains'],
            'trading_pair__base_asset__type': ['exact', 'icontains'],
            'trading_pair__quote_asset__type': ['exact', 'icontains'],
            'trading_pair__base_asset__market': ['exact', 'icontains'],
            'trading_pair__quote_asset__market': ['exact', 'icontains'],
            'trading_pair__traded': ['exact'],
            'is_closed': ['exact'],
            'side': ['exact'],
            'opened_at': ['exact', 'gt', 'lt'],
            'closed_at': ['exact', 'gt', 'lt'],
        }
