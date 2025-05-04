from django.db import models

from accounting.models.enams import PositionSide
from users.models import User
from core.models import TimestampedModel


class Position(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name='Пользователь',
    )
    trading_pair = models.CharField(
        'Торговая пара',
        max_length=20,
        help_text='Торговая пара (например, BTCUSDT)',
    )
    side = models.CharField(
        'Направление',
        max_length=10,
        choices=PositionSide.choices,
    )
    size = models.DecimalField(
        'Размер',
        max_digits=20,
        decimal_places=8,
    )
    position_value = models.DecimalField(
        'Стоимость позиции',
        max_digits=20,
        decimal_places=8,
    )
    entry_price = models.DecimalField(
        'Цена входа',
        max_digits=20,
        decimal_places=8,
    )
    mark_price = models.DecimalField(
        'Маркированная цена',
        max_digits=20,
        decimal_places=8,
        help_text='Текущая рыночная цена, используемая для оценки позиции',
    )
    leverage = models.DecimalField(
        'Кредитное плечо',
        max_digits=10,
        decimal_places=2,
    )
    position_im = models.DecimalField(
        'Начальная маржа',
        max_digits=20,
        decimal_places=8,
        help_text='Начальное требование по марже для открытия позиции',
    )
    position_mm = models.DecimalField(
        'Маржа поддержки',
        max_digits=20,
        decimal_places=8,
        help_text='Минимальная маржа, необходимая для поддержания открытой позиции',
    )
    liq_price = models.DecimalField(
        'Цена ликвидации',
        max_digits=20,
        decimal_places=8,
        null=True,
        blank=True,
        help_text='Цена, при достижении которой позиция будет ликвидирована системой',
    )
    take_profit = models.DecimalField(
        'Тейк-профит',
        max_digits=20,
        decimal_places=8,
        null=True,
        blank=True,
    )
    stop_loss = models.DecimalField(
        'Стоп-лосс',
        max_digits=20,
        decimal_places=8,
        null=True,
        blank=True,
    )
    trailing_stop = models.DecimalField(
        'Трейлинг-стоп',
        max_digits=20,
        decimal_places=8,
        null=True,
        blank=True,
    )
    unrealised_pnl = models.DecimalField(
        'Нереализованный PnL',
        max_digits=20,
        decimal_places=8,
        help_text='Текущая нереализованная (бумажная) прибыль или убыток по позиции',
    )
    cur_realised_pnl = models.DecimalField(
        'Текущий реализованный PnL',
        max_digits=20,
        decimal_places=8,
        help_text='Прибыль или убыток, реализованные с момента открытия позиции',
    )
    cum_realised_pnl = models.DecimalField(
        'Накопл. реализ. PnL',
        max_digits=20,
        decimal_places=8,
        help_text='Кумулятивная сумма реализованной прибыли или убытка с момента открытия позиции',
    )
    session_avg_price = models.DecimalField(
        'Ср. цена сессии',
        max_digits=20,
        decimal_places=8,
        null=True,
        blank=True,
        help_text='Средняя цена входа за текущую торговую сессию',
    )
    data_created_time = models.DateTimeField(
        'Время создания позиции',
    )
    data_updated_time = models.DateTimeField(
        'Время обновления позиции',
    )

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'

    def __str__(self):
        return f'Позиция {self.trading_pair} ({self.side})'

    @property
    def is_open(self) -> bool:
        return self.size > 0
