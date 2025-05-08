from django.db import models


class AssetType(models.TextChoices):
    """Тип актива"""

    STOCK = 'ST', 'Акция'
    CURRENCY = 'CR', 'Валюта'
    CRYPTOCURRENCY = 'CC', 'Криптовалюта'


class MarketType(models.TextChoices):
    """Рынок"""

    SPOT = 'SP', 'Спот'
    FUTURES = 'FU', 'Фьючерсы'
    OPTIONS = 'OP', 'Опционы'
    MARGIN = 'MA', 'Маржинальная торговля'


class Exchange(models.TextChoices):
    """Биржа"""

    BYBIT = 'ByBit', 'ByBit'
    KUCOIN = 'KuCoin', 'KuCoin'


class PositionSide(models.TextChoices):
    """Сторона позиции"""

    LONG = 'LONG', 'Long'
    SHORT = 'SHORT', 'Short'
