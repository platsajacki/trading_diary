from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError

if TYPE_CHECKING:
    from accounting.models.finances import FinancialAsset


def validate_compatible_assets(base_asset: FinancialAsset, quote_asset: FinancialAsset) -> None:
    """
    Проверяет совместимость двух финансовых активов и вызывает исключение, если они несовместимы.

    Аргументы:
        base_asset (FinancialAsset): Базовый финансовый актив для проверки.
        quote_asset (FinancialAsset): Котируемый финансовый актив для проверки.

    Исключения:
        ValidationError: Если активы несовместимы по бирже, типу или рынку.
    """
    if not base_asset.is_compatible_with(quote_asset):
        raise ValidationError('Нельзя создать торговую пару с активами с разными биржами, типами или рынками.')
