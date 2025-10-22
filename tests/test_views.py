import pytest
import pandas as pd
from unittest.mock import patch
from datetime import datetime
from src.views import build_main_response


@pytest.fixture
def mock_data():
    # Пример DataFrame с транзакционными данными, например, с Номером карты, Категорией и Описанием
    data = {
        "Дата операции": ["2023-01-01 12:00:00", "2023-01-02 14:00:00"],
        "Сумма операции": [-100, -200],
        "Номер карты": ["*1234", "*5678"],
        "Категория": ["Food", "Entertainment"],
        "Описание": ["Покупка еды", "Покупка билета на концерт"]
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_settings():
    return {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "GOOGL"],
    }


def test_build_main_response_success(mock_data, mock_settings):
    date_str = "2023-01-01 12:00:00"

    with patch('src.services.get_card_spent') as mock_get_card_spent, \
            patch('src.services.get_top_transactions') as mock_get_top_transactions, \
            patch('src.market_apis.get_currency_rates') as mock_get_currency_rates, \
            patch('src.market_apis.get_stock_prices') as mock_get_stock_prices, \
            patch('src.services.filter_df_by_month') as mock_filter_df_by_month:
        # Настройка возвращаемых значений
        mock_filter_df_by_month.return_value = mock_data
        mock_get_card_spent.return_value = [{"amount": -100, "category": "Food", "last_digits": "*1234"}]
        mock_get_top_transactions.return_value = [
            {"amount": -50, "description": "Покупка еды", "category": "Food"}
        ]
        mock_get_currency_rates.return_value = [{"currency": "USD", "rate": 75}, {"currency": "EUR", "rate": 94.75}]
        mock_get_stock_prices.return_value = [{"symbol": "AAPL", "price": 150}]

        response = build_main_response(date_str, mock_data, mock_settings)

        assert response["greeting"] == "Добрый день"  # Приветствие в зависимости от времени
        assert len(response["cards"]) == 1  # Проверка количества карт
        assert len(response["top_transactions"]) == 1  # Проверка количества топ-транзакций
        assert len(response["currency_rates"]) == 2  # Проверка количества курсов валют
        assert response["currency_rates"][0]["currency"] == "USD"  # Проверка валюты USD
        assert response["currency_rates"][1]["currency"] == "EUR"  # Проверка валюты EUR


def test_build_main_response_stock_error(mock_data, mock_settings):
    date_str = "2023-01-01 18:00:00"

    with patch('src.services.get_card_spent') as mock_get_card_spent, \
            patch('src.services.get_top_transactions') as mock_get_top_transactions, \
            patch('src.market_apis.get_currency_rates') as mock_get_currency_rates, \
            patch('src.market_apis.get_stock_prices',
                  side_effect=Exception("Stock API Error")) as mock_get_stock_prices, \
            patch('src.services.filter_df_by_month') as mock_filter_df_by_month:
        # Настройка возвращаемых значений
        mock_filter_df_by_month.return_value = mock_data
        mock_get_card_spent.return_value = [{"amount": -100, "category": "Food"}]
        mock_get_top_transactions.return_value = [{"amount": -50, "description": "Top Expense"}]
        mock_get_currency_rates.return_value = [{"currency": "USD", "rate": 75}]

        response = build_main_response(date_str, mock_data, mock_settings)

        assert response["greeting"] == "Добрый вечер"  # Приветствие в зависимости от времени
        assert len(response["stock_prices"]) == 0  # Ожидаем пустой список котировок акций
