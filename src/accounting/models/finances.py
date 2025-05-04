from typing import Any

from django.db import models
from django.db.models import UniqueConstraint

from accounting.models.enams import AssetType, Exchange, MarketType
from accounting.validators import validate_compatible_assets
from core.models import TimestampedModel


class FinancialAsset(TimestampedModel):
    """
    Модель, представляющая финансовый актив.

    Атрибуты:
        ticker (str): Тикер актива, уникальный идентификатор.
        type (str): Тип актива, например, акция, валюта или криптовалюта.
        market (str): Рынок, на котором торгуется актив, например, спот или фьючерсы.
        exchange (str): Биржа, на которой зарегистрирован актив.

    Методы:
        is_compatible_with(other: 'FinancialAsset') -> bool:
            Проверяет, совместим ли этот актив с другим активом по типу, бирже и рынку.
    """

    ticker = models.CharField(
        'Тикер',
        max_length=50,
        db_index=True,
    )
    type = models.CharField(
        'Тип актива',
        max_length=2,
        choices=AssetType.choices,
    )
    market = models.CharField(
        'Рынок',
        max_length=2,
        choices=MarketType.choices,
    )
    exchange = models.CharField(
        'Биржа',
        max_length=50,
        choices=Exchange.choices,
    )

    def __str__(self) -> str:
        return f'{self.ticker}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.ticker}, {self.market})'

    def is_compatible_with(self, other: 'FinancialAsset') -> bool:
        """Проверяет, совместим ли этот актив с другим активом по типу, бирже и рынку.

        Аргументы:
            other (FinancialAsset): Другой финансовый актив для проверки совместимости.

        Возвращает:
            bool: True, если активы совместимы, иначе False.
        """
        if not isinstance(other, FinancialAsset):
            return NotImplemented
        return self.exchange == other.exchange and self.type == other.type and self.market == other.market

    class Meta:
        verbose_name = 'Финансовый актив'
        verbose_name_plural = 'Финансовые активы'
        constraints = [
            UniqueConstraint(
                fields=['ticker', 'type', 'market', 'exchange'],
                name='unique_asset',
            )
        ]


class TradingPair(TimestampedModel):
    """
    Модель, представляющая торговую пару.

    Атрибуты:
        base_asset (ForeignKey): Базовый актив в паре.
        quote_asset (ForeignKey): Котируемый актив в паре.
        traded (bool): Флаг, указывающий, торгуется ли пара.

    Методы:
        clean() -> None:
            Выполняет валидацию торговой пары, проверяя совместимость активов.
        save(*args: Any, **kwargs: Any) -> None:
            Сохраняет объект после проверки на валидность.
        symbol() -> str:
            Возвращает символ (текер) торговой пары, представляющий комбинацию тикеров базового и котируемого активов.
    """

    base_asset = models.ForeignKey(
        FinancialAsset,
        on_delete=models.CASCADE,
        related_name='base_trading_pairs',
        verbose_name='Базовый актив',
    )
    quote_asset = models.ForeignKey(
        FinancialAsset,
        on_delete=models.CASCADE,
        related_name='quote_trading_pairs',
        verbose_name='Котируемый актив',
    )
    traded = models.BooleanField(
        'Торгуется',
        default=True,
    )

    def clean(self) -> None:
        """Проверяет, что базовый и котируемый активы совместимы."""
        validate_compatible_assets(self.base_asset, self.quote_asset)

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Переопределяет стандартный метод save, добавляя предварительную проверку."""
        self.clean()
        super().save(*args, **kwargs)

    @property
    def symbol(self) -> str:
        """
        Возвращает символ торговой пары.

        Символ составляется из тикеров базового и котируемого активов, например: 'BTCUSDT'.
        """
        return f'{self.base_asset.ticker}{self.quote_asset.ticker}'

    class Meta:
        verbose_name = 'Торговая пара'
        verbose_name_plural = 'Торговые пары'
        constraints = [
            UniqueConstraint(
                fields=[
                    'base_asset',
                    'quote_asset',
                ],
                name='unique_pair',
            )
        ]

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.base_asset}, {self.quote_asset})'
