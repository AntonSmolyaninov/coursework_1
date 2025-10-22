import logging
import os
import time

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def get_currency_rates(currency_list: list[str]) -> list[dict]:
    """
    Получает курсы валют к рублю по списку currency_list (например ['USD', 'EUR']).
    Использует API Центробанка РФ.
    """
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()  # Проверяем статус ответа
        data = resp.json().get("Valute", {})

        rates = []
        for code in currency_list:
            rate_info = data.get(code)
            if rate_info:
                rates.append({
                    "currency": code,
                    "rate": round(rate_info["Value"], 2)
                })
        logger.info(f"Получены курсы валют: {rates}")
        return rates
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к API: {e}")
        return []
    except KeyError as e:
        logger.error(f"Неверный ответ от API: отсутствует ключ {e}")
        return []
    except Exception as e:
        logger.error(f"Ошибка получения курсов валют: {e}")
        return []


def get_stock_prices(stock_list: list[str]) -> list[dict]:
    """
    Получает цены акций с помощью Alpha Vantage API.
    API-ключ берётся только из .env (переменная API_KEY_AV)
    :param stock_list: список тикеров (например, ['AAPL', 'TSLA'])
    :return: список словарей вида {"stock": "AAPL", "price": 172.23}
    """
    api_key = os.environ.get("API_KEY_AV")
    if not api_key:
        raise ValueError("API_KEY_AV не найден в .env! Пожалуйста, добавьте его в .env файл.")

    url = "https://www.alphavantage.co/query"
    prices = []
    for i, symbol in enumerate(stock_list):
        params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": api_key}
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            quote = data.get("Global Quote", {})
            price = round(float(quote.get("05. price", 0)), 2)
            prices.append({"stock": symbol, "price": price})
            logger.info(f"Получена цена для {symbol}: {price}")
        except Exception as e:
            logger.error(f"Ошибка получения цены для {symbol}: {e}")
            prices.append({"stock": symbol, "price": None})
        # Ограничение бесплатного тарифа: не больше 5 запросов в минуту!
        if i < len(stock_list) - 1:
            time.sleep(12.5)
    return prices
