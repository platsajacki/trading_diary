from app.celery import celery_app
from bybit.services.celery import LinearUSDTGetter


@celery_app.task
def get_current_usdt_linear_instruments() -> None:
    """
    Получает список актуальных линейных фьючерсных контрактов, торгуемых к USDT.
    Обрабатывет их и записывает в базу.
    Если какие фьючерсы перестают обслуживаться, то удаляет из базы.
    """
    LinearUSDTGetter()()
