from typing import Any

from django.db.transaction import atomic

from accounting.models import FinancialAsset, TradingPair
from bybit.connections import public_bybit
from bybit.constants import FUTURES_BYBIT_DATA, LINEAR, USDT
from core.services.interfaces import DataPipelineService


class LinearUSDTGetter(DataPipelineService):
    """
    Сервис для получения и обработки информации о линейных фьючерсах USDT на бирже Bybit.

    Методы:
        process_data(data: dict) -> list[str]:
            Обрабатывает полученные данные, фильтруя активы, которые соответствуют линейным фьючерсам USDT.

        fetch_data() -> dict:
            Выполняет HTTP-запрос к Bybit API для получения информации о торговых инструментах.

        get_new_assets(coins: Any) -> list[FinancialAsset]:
            Находит активы, которых еще нет в базе данных, и возвращает их в виде списка объектов `FinancialAsset`.

        save_to_database(coins: Any) -> None:
            Сохраняет новые активы в базу данных и создает торговые пары с USDT.
    """

    def process_data(self, data: dict) -> list[str]:
        """
        Обрабатывает данные, фильтрует линейные фьючерсы USDT.

        Аргументы:
            data (dict): Данные с информацией о торговых инструментах.

        Возвращает:
            list[str]: Список тикеров активов, которые соответствуют критериям линейных фьючерсов USDT.
        """
        symbols_data = data['result']['list']
        tikers = []
        for symbol_data in symbols_data:
            symbol = symbol_data['symbol']
            if symbol_data['quoteCoin'] != USDT or symbol_data['isPreListing']:
                continue
            tikers.append(symbol[:-4])
        return tikers

    def fetch_data(self) -> dict:
        """
        Выполняет запрос к API Bybit для получения данных о линейных фьючерсах.

        Возвращает:
            dict: Данные о доступных торговых инструментах.
        """
        return public_bybit.get_instruments_info(category=LINEAR, limit=1000)

    def get_new_assets(self, coins: Any) -> list[FinancialAsset]:
        """
        Возвращает список новых активов, которые еще не существуют в базе данных и создает их.

        Аргументы:
            coins (Any): Список тикеров активов для проверки существования.

        Возвращает:
            list[FinancialAsset]: Список созданных объектов `FinancialAsset`, которые были добавлены в базу данных.
        """
        existing_assets = FinancialAsset.objects.filter(ticker__in=coins, **FUTURES_BYBIT_DATA)
        existing_tickers = set(existing_assets.values_list('ticker', flat=True))
        new_tickers = set(coins) - existing_tickers
        new_assets = [FinancialAsset(ticker=ticker, **FUTURES_BYBIT_DATA) for ticker in new_tickers]
        return FinancialAsset.objects.bulk_create(new_assets)

    def update_trading_pairs(self, coins: Any, usdt: FinancialAsset) -> None:
        """
        Обновляет торговые пары в базе данных, удаляя те, которые больше не существуют.

        Аргументы:
            coins (Any): Список тикеров активов для обновления.

        В случае ошибки все изменения откатываются.
        """
        trading_pairs = TradingPair.objects.filter(traded=True, quote_asset=usdt).exclude(base_asset__ticker__in=coins)
        trading_pairs.update(traded=False)

    @atomic
    def save_to_database(self, coins: Any) -> None:
        """
        Сохраняет новые финансовые активы и создает торговые пары с USDT в базе данных.

        Аргументы:
            coins (Any): Список тикеров активов для сохранения.

        В рамках транзакции:
        - Сначала проверяются и создаются новые активы с помощью метода `get_new_assets`.
        - Затем создаются новые торговые пары с базовым активом и USDT как валютой котировки.

        В случае ошибки все изменения откатываются.
        """
        usdt, _ = FinancialAsset.objects.get_or_create(ticker=USDT, **FUTURES_BYBIT_DATA)
        pairs = []
        self.update_trading_pairs(coins, usdt)
        new_assets = self.get_new_assets(coins)
        for asset in new_assets:
            pairs.append(TradingPair(base_asset=asset, quote_asset=usdt))
        if pairs:
            TradingPair.objects.bulk_create(pairs, ignore_conflicts=True)
