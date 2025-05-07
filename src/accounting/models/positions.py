from django.db import models

from accounting.managers.positions import PositionManager
from accounting.models.enams import PositionSide
from accounting.models.finances import TradingPair
from core.models import TimestampedModel
from users.models import User


class Position(TimestampedModel):
    """Модель для хранения информации о позициях пользователя на бирже."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name='Пользователь',
    )
    trading_pair = models.ForeignKey(
        TradingPair,
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name='Торговая пара',
    )
    is_closed = models.BooleanField(
        'Закрыта',
        default=False,
        help_text='Флаг, указывающий, закрыта ли позиция',
    )
    mark_price = models.DecimalField(
        'Маркированная цена',
        max_digits=22,
        decimal_places=10,
        help_text='Текущая рыночная цена, используемая для оценки позиции',
    )
    side = models.CharField(
        'Направление',
        max_length=10,
        choices=PositionSide.choices,
    )
    size = models.DecimalField(
        'Размер',
        max_digits=22,
        decimal_places=10,
    )
    position_value = models.DecimalField(
        'Стоимость позиции',
        max_digits=22,
        decimal_places=10,
    )
    entry_price = models.DecimalField(
        'Цена входа',
        max_digits=22,
        decimal_places=10,
    )
    leverage = models.DecimalField(
        'Кредитное плечо',
        max_digits=10,
        decimal_places=2,
    )
    liq_price = models.DecimalField(
        'Цена ликвидации',
        max_digits=22,
        decimal_places=10,
        null=True,
        blank=True,
        help_text='Цена, при достижении которой позиция будет ликвидирована системой',
    )
    take_profit = models.DecimalField(
        'Тейк-профит',
        max_digits=22,
        decimal_places=10,
        null=True,
        blank=True,
    )
    stop_loss = models.DecimalField(
        'Стоп-лосс',
        max_digits=22,
        decimal_places=10,
        null=True,
        blank=True,
    )
    trailing_stop = models.DecimalField(
        'Трейлинг-стоп',
        max_digits=22,
        decimal_places=10,
        null=True,
        blank=True,
    )
    session_avg_price = models.DecimalField(
        'Ср. цена сессии',
        max_digits=22,
        decimal_places=10,
        null=True,
        blank=True,
        help_text='Средняя цена входа за текущую торговую сессию',
    )
    opened_at = models.DateTimeField(
        'Время создания позиции',
    )
    closed_at = models.DateTimeField(
        'Время закрытия позиции',
        null=True,
        blank=True,
    )

    objects: PositionManager = PositionManager()

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'

    def __str__(self):
        return f'Позиция {self.trading_pair} ({self.side})'
