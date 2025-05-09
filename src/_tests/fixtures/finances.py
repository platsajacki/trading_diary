import pytest

from _tests import FixtureFactory
from apps.accounting.models import FinancialAsset, TradingPair
from apps.accounting.models.enams import AssetType, Exchange, MarketType


def get_bybit_financial_asset_schema(
    factory: FixtureFactory, market: MarketType, exchange: Exchange, iterations: int = 10
) -> list[dict]:
    return factory.schema(
        lambda: {
            'ticker': factory.field('word'),
            'type': AssetType.CURRENCY,
            'market': market,
            'exchange': exchange,
        },
        iterations=iterations,
    ).create()


@pytest.fixture
def bybit_futures_financial_asset_data(factory: FixtureFactory) -> list[dict]:
    return get_bybit_financial_asset_schema(factory, market=MarketType.FUTURES, exchange=Exchange.BYBIT)


@pytest.fixture
def bybit_spot_financial_asset_data(factory: FixtureFactory) -> list[dict]:
    return get_bybit_financial_asset_schema(factory, market=MarketType.SPOT, exchange=Exchange.BYBIT)


@pytest.fixture
def bybit_futures_financial_assets(bybit_futures_financial_asset_data: list[dict]) -> list[FinancialAsset]:
    assets = [FinancialAsset(**data) for data in bybit_futures_financial_asset_data]
    return FinancialAsset.objects.bulk_create(assets)


@pytest.fixture
def bybit_spot_financial_assets(bybit_spot_financial_asset_data: list[dict]) -> list[FinancialAsset]:
    assets = [FinancialAsset(**data) for data in bybit_spot_financial_asset_data]
    return FinancialAsset.objects.bulk_create(assets)


def create_trading_pairs(financial_assets: list[FinancialAsset]) -> list[TradingPair]:
    """
    Делит список финансовых активов на две равные части и создает торговые пары,
    используя первые половину как base_asset и вторую как quote_asset.

    Если количество активов нечётное, лишние активы игнорируются.
    """
    pairs = []
    n = len(financial_assets)
    half = n // 2
    first_half = financial_assets[:half]
    second_half = financial_assets[half : half * 2]
    for base_asset, quote_asset in zip(first_half, second_half):
        pairs.append(
            TradingPair(
                base_asset=base_asset,
                quote_asset=quote_asset,
            )
        )
    return TradingPair.objects.bulk_create(pairs)


@pytest.fixture
def bybit_futures_trading_pairs(bybit_futures_financial_assets: list[FinancialAsset]) -> list[TradingPair]:
    return create_trading_pairs(bybit_futures_financial_assets)


@pytest.fixture
def bybit_spot_trading_pairs(bybit_spot_financial_assets: list[FinancialAsset]) -> list[TradingPair]:
    return create_trading_pairs(bybit_spot_financial_assets)
