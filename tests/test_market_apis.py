import pytest
from unittest.mock import patch
from src.market_apis import get_currency_rates, get_stock_prices


# Тест для функции get_currency_rates
def test_get_currency_rates_success():
    currency_list = ['USD', 'EUR']

    with patch('requests.get') as mock_get:
        # Настройка мока
        mock_response = {
            "Valute": {
                "USD": {"Value": 75.15},
                "EUR": {"Value": 85.25}
            }
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = lambda: None  # Убираем проверку статуса

        # Вызов функции
        result = get_currency_rates(currency_list)

        # Проверка результата
        assert len(result) == 2
        assert result[0]['currency'] == 'USD'
        assert result[0]['rate'] == 75.15
        assert result[1]['currency'] == 'EUR'
        assert result[1]['rate'] == 85.25


def test_get_currency_rates_failure():
    currency_list = ['USD', 'EUR']

    with patch('requests.get') as mock_get:
        # Настройка мока для ошибки
        mock_get.side_effect = Exception("Ошибка запроса")

        # Вызов функции
        result = get_currency_rates(currency_list)

        # Проверка результата
        assert result == []


# Тест для функции get_stock_prices
def test_get_stock_prices_success():
    stock_list = ['AAPL', 'TSLA']
    api_key = "test_api_key"

    with patch('os.environ.get', return_value=api_key), patch('requests.get') as mock_get:
        # Настройка мока
        mock_response = {
            "Global Quote": {
                "05. price": "150.00"
            }
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = lambda: None  # Убираем проверку статуса

        # Вызов функции
        result = get_stock_prices(stock_list)

        # Проверка результата
        assert len(result) == 2
        assert result[0]['stock'] == 'AAPL'
        assert result[0]['price'] == 150.00
        assert result[1]['stock'] == 'TSLA'
        assert result[1]['price'] == 150.00


def test_get_stock_prices_no_api_key():
    stock_list = ['AAPL', 'TSLA']

    with patch('os.environ.get', return_value=None):
        with pytest.raises(ValueError) as excinfo:
            get_stock_prices(stock_list)
        assert str(excinfo.value) == "API_KEY_AV не найден в .env! Пожалуйста, добавьте его в .env файл."


def test_get_stock_prices_failure():
    stock_list = ['AAPL']
    api_key = "test_api_key"

    with patch('os.environ.get', return_value=api_key), patch('requests.get') as mock_get:
        # Настройка мока для ошибки
        mock_get.side_effect = Exception("Ошибка запроса")

        # Вызов функции
        result = get_stock_prices(stock_list)

        # Проверка результата
        assert result[0]['stock'] == 'AAPL'
        assert result[0]['price'] is None  # Ожидаем, что цена будет None из-за ошибки
