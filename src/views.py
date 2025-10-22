import logging
from datetime import datetime
import pandas as pd
from src.market_apis import get_currency_rates, get_stock_prices
from src.services import filter_df_by_month, get_card_spent, get_top_transactions

logger = logging.getLogger(__name__)


def get_greeting(dt: datetime) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    :param dt: Объект datetime, который использован для определения текущего часа.
    :return: Строка с приветствием: "Доброе утро", "Добрый день", "Добрый вечер" или "Доброй ночи".
    """
    hour = dt.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def build_main_response(date_str: str, df: pd.DataFrame, settings: dict) -> dict:
    """
    Формирует основной JSON-ответ для дашборда пользователя на заданную дату.

    :param date_str: Строка, представляющая дату и время в формате "YYYY-MM-DD HH:MM:SS".
    :param df: DataFrame с данными транзакций пользователя.
    :param settings: Словарь, содержащий настройки пользователя, включая валюты и акции.
    :return: Словарь с приветствием, картами, топ-транзакциями, курсами валют и акциями.
    """
    logger.info(f"Начало формирования главного JSON-ответа на дату {date_str}")

    # Преобразование строки даты в объект datetime
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    # Прочие операции
    df_period = filter_df_by_month(df, date_str)
    logger.info(f"Отфильтрованные данные за месяц: {df_period}")

    cards = get_card_spent(df_period)
    logger.info(f"Картные транзакции: {cards}")

    top_transactions = get_top_transactions(df_period, 5)
    logger.info(f"Топ-транзакции: {top_transactions}")

    try:
        currency_rates = get_currency_rates(settings["user_currencies"])
        logger.info("Курсы валют успешно получены")
    except Exception as e:
        logger.error(f"Ошибка получения курса валют: {e}")
        currency_rates = []

    try:
        stock_prices = get_stock_prices(settings["user_stocks"])
        logger.info("Котировки акций успешно получены")
    except Exception as e:
        logger.error(f"Ошибка получения котировок акций: {e}")
        stock_prices = []

    # Готовим ответ, используя правильное приветствие
    response = {
        "greeting": get_greeting(dt),  # Используем get_greeting для динамического приветствия
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    logger.info("Главный JSON-ответ сформирован")
    return response
