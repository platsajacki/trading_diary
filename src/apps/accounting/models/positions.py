from decimal import Decimal

from django.db import models

from apps.accounting.managers.positions import PositionManager
from apps.accounting.models.enums import PositionSide, TralingStopType
from apps.accounting.models.finances import TradingPair
from apps.core.models import TimestampedModel
from apps.users.models import User


class Position(TimestampedModel):
    """
    Модель для хранения информации о позициях пользователя на бирже.

    Позиция привязана к рынку через торговую пару. Торговая пара, в свою очередь, через финансовый инструмент.
    """

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
    type_trailing_stop = models.CharField(
        'Тип трейлинг-стопа',
        max_length=20,
        choices=TralingStopType.choices,
        null=True,
        blank=True,
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
        ordering = ['-opened_at']

    def __str__(self):
        return f'Позиция {self.trading_pair} ({self.side})'

    @property
    def position_value(self) -> Decimal:
        """Возвращает стоимость позиции."""
        position_value = self.size * self.entry_price
        if self.leverage:
            position_value /= self.leverage
        return position_value

    def clean_traling_stop(self) -> None:
        """Проверяет корректность трейлинг-стопа."""
        if self.trailing_stop and not self.type_trailing_stop:
            raise ValueError('Type of trailing stop must be set if trailing stop is provided.')

    def clean(self) -> None:
        """Проверяет корректность данных перед сохранением."""
        self.clean_traling_stop()
        return super().clean()


class PositionComment(TimestampedModel):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Позиция',
    )
    chart_link = models.URLField(
        'Ссылка на график',
        null=True,
        blank=True,
        help_text='Ссылка на график, к которому относится комментарий',
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        max_length=2048,
    )

    class Meta:
        verbose_name = 'Комментарий к позиции'
        verbose_name_plural = 'Комментарии к позициям'
        ordering = ['-created_at']

    def __str__(self):
        return f'Комментарий для {self.position} от {self.created_at:%H:%M %Y-%m-%d}'
