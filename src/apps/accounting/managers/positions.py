from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import CharField, F, Manager, QuerySet
from django.db.models.functions import Concat

from apps.accounting.models.enums import Exchange, MarketType

if TYPE_CHECKING:
    from apps.accounting.models import Position
    from apps.users.models import User


class PositionQuerySet(QuerySet['Position']):
    def with_select_related(self) -> PositionQuerySet:
        return self.select_related(
            'trading_pair',
            'user',
            'trading_pair__base_asset',
            'trading_pair__quote_asset',
        )

    def annotate_symbol(self) -> PositionQuerySet:
        return self.annotate(
            pair_symbol=Concat(
                F('trading_pair__base_asset__ticker'),
                F('trading_pair__quote_asset__ticker'),
                output_field=CharField(),
            )
        )

    def get_by_symbol(self, symbol: str, market: MarketType, exchange: Exchange | str) -> Position | None:
        return (
            self.annotate_symbol()
            .with_select_related()
            .filter(
                pair_symbol=symbol,
                trading_pair__base_asset__market=market,
                trading_pair__quote_asset__market=market,
                trading_pair__quote_asset__exchange=exchange,
                trading_pair__base_asset__exchange=exchange,
            )
            .first()
        )

    def get_by_user(self, user: User) -> PositionQuerySet:
        return self.filter(user=user).with_select_related().annotate_symbol()

    def with_commets(self) -> PositionQuerySet:
        return self.prefetch_related('comments').order_by('-comments__created_at')


class PositionManager(Manager['Position']):
    def get_queryset(self) -> PositionQuerySet:
        return PositionQuerySet(self.model, using=self._db)

    def with_select_related(self) -> PositionQuerySet:
        return self.get_queryset().with_select_related()

    def annotate_symbol(self) -> PositionQuerySet:
        return self.get_queryset().annotate_symbol()

    def get_by_symbol(self, symbol: str, market: MarketType, exchange: Exchange | str) -> Position | None:
        return self.get_queryset().get_by_symbol(symbol, market, exchange)

    def get_by_user(self, user: User) -> PositionQuerySet:
        return self.get_queryset().get_by_user(user)
