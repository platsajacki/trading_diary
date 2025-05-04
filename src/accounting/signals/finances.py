from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounting.models.finances import FinancialAsset, TradingPair
from accounting.validators import validate_compatible_assets


@receiver(post_save, sender=FinancialAsset)
def validate_related_trading_pairs(sender: FinancialAsset, instance: FinancialAsset, **kwargs: Any) -> None:
    """
    Проверяет совместимость всех торговых пар, связанных с финансовым активом, после его сохранения.

    Аргументы:
        sender (FinancialAsset): Класс модели, отправляющей сигнал (в данном случае FinancialAsset).
        instance (FinancialAsset): Экземпляр финансового актива, который был сохранен.
        kwargs (Any): Дополнительные аргументы сигнала.

    Описание:
        Функция проверяет все торговые пары, где данный финансовый актив выступает либо как базовый актив,
        либо как котируемый актив. Если какие-либо пары несовместимы, будет вызвано исключение через
        функцию `validate_compatible_assets`.
    """
    trading_pairs = TradingPair.objects.filter(base_asset=instance) | TradingPair.objects.filter(quote_asset=instance)
    for pair in trading_pairs:
        validate_compatible_assets(pair.base_asset, pair.quote_asset)
