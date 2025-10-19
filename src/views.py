import logging
from datetime import datetime

import pandas as pd

from src.market_apis import get_currency_rates, get_stock_prices
from src.services import filter_df_by_month, get_card_spent, get_top_transactions

logger = logging.getLogger(__name__)


def get_greeting(dt: datetime) -> str:
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
       Возвращает:
           dict: Словарь с приветствием, картами, топ-транзакциями, курсами валют и акциями.
       """
    logger.info(f"Начало формирования главного JSON-ответа на дату {date_str}")
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    df_period = filter_df_by_month(df, date_str)
    cards = get_card_spent(df_period)
    top_transactions = get_top_transactions(df_period, 5)
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
    response = {
        "greeting": get_greeting(dt),
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    logger.info("Главный JSON-ответ сформирован")
    return response
