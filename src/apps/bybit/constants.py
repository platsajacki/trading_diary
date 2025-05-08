from os import getenv

from accounting.models.finances import AssetType, Exchange, MarketType

USDT = 'USDT'
LINEAR = 'linear'

TESTNET = bool(int(getenv('NOT_TESTNET', 1)))

FUTURES_BYBIT_DATA = {
    'type': AssetType.CRYPTOCURRENCY.value,
    'market': MarketType.FUTURES.value,
    'exchange': Exchange.BYBIT.value,
}
