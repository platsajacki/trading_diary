from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import CharField, F, Manager, QuerySet
from django.db.models.functions import Concat

if TYPE_CHECKING:
    from apps.accounting.models.enums import Exchange, MarketType
    from apps.accounting.models.finances import TradingPair


class TradingPairQuerySet(QuerySet['TradingPair']):
    def with_select_related(self) -> TradingPairQuerySet:
        return self.select_related('base_asset', 'quote_asset')

    def annotate_symbol(self) -> TradingPairQuerySet:
        return self.annotate(
            pair_symbol=Concat(
                F('base_asset__ticker'),
                F('quote_asset__ticker'),
                output_field=CharField(),
            )
        )

    def get_by_symbol(self, symbol: str, market: MarketType | str, exchange: Exchange | str) -> TradingPair | None:
        return (
            self.annotate_symbol()
            .filter(
                pair_symbol=symbol,
                base_asset__market=market,
                quote_asset__market=market,
                base_asset__exchange=exchange,
                quote_asset__exchange=exchange,
            )
            .with_select_related()
            .first()
        )


class TradingPairManager(Manager['TradingPair']):
    def get_queryset(self) -> TradingPairQuerySet:
        return TradingPairQuerySet(self.model, using=self._db)

    def get_by_symbol(self, symbol: str, market: MarketType | str, exchange: Exchange | str) -> TradingPair | None:
        return self.get_queryset().get_by_symbol(symbol, market, exchange)

    def with_select_related(self) -> TradingPairQuerySet:
        return self.get_queryset().with_select_related()
