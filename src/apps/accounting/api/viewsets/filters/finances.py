from apps.accounting.models import TradingPair
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
