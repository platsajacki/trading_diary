from django.contrib import admin

from accounting.models import FinancialAsset, TradingPair
from accounting.models.positions import Position


@admin.register(FinancialAsset)
class FinancialAssetAdmin(admin.ModelAdmin):
    """Административная модель для управления финансовыми активами."""

    list_display = (
        'ticker',
        'exchange',
        'type',
        'market',
    )
    list_filter = (
        'type',
        'market',
        'exchange',
    )
    search_fields = (
        'ticker',
        'exchange',
    )
    ordering = ('ticker',)


@admin.register(TradingPair)
class TradingPairAdmin(admin.ModelAdmin):
    """Административная модель для управления торговыми парами."""

    list_display = (
        'symbol',
        'base_asset',
        'quote_asset',
        'traded',
    )
    list_filter = (
        'traded',
        'base_asset',
        'quote_asset',
    )
    search_fields = (
        'base_asset__ticker',
        'quote_asset__ticker',
    )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'trading_pair',
        'user',
        'side',
        'size',
        'entry_price',
        'mark_price',
        'leverage',
        'opened_at',
        'closed_at',
    )
    list_filter = ('side', 'trading_pair')
    search_fields = ('trading_pair', 'side')
