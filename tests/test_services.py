import pytest
import pandas as pd
from src.services import filter_df_by_month, get_card_spent, get_top_transactions, search_transactions

# Подготовка тестовых данных
@pytest.fixture
def sample_data():
    data = {
        "Дата операции": [
            "2023-01-15 12:00:00",
            "2023-01-20 14:30:00",
            "2023-02-10 09:00:00",
            "2023-03-15 17:45:00",
            "2023-01-25 10:15:00"
        ],
        "Номер карты": [
            "1234567812345678",
            "8765432187654321",
            "1234567812345678",
            "8765432187654321",
            "1234567812345678"
        ],
        "Сумма операции": [
            100.00,
            200.00,
            150.00,
            50.00,
            75.00
        ],
        "Категория": [
            "Еда",
            "Транспорт",
            "Еда",
            "Развлечения",
            "Еда"
        ],
        "Описание": [
            "Ужин в ресторане",
            "Поездка на такси",
            "Заказ пиццы",
            "Кино",
            "Закупка продуктов"
        ]
    }
    return pd.DataFrame(data)

def test_filter_df_by_month(sample_data):
    result = filter_df_by_month(sample_data, "2023-01-31 23:59:59")
    expected_len = 3  # Ожидаем, что будет 3 операции в январе
    assert len(result) == expected_len

def test_get_card_spent(sample_data):
    result = get_card_spent(sample_data)
    expected_result = [
        {'last_digits': '5678', 'total_spent': 325.0, 'cashback': 3.25},
        {'last_digits': '4321', 'total_spent': 250.0, 'cashback': 2.5}
    ]
    assert result == expected_result

def test_get_top_transactions(sample_data):
    result = get_top_transactions(sample_data, n=2)
    expected_result = [
        {"date": "20.01.2023", "amount": 200.00, "category": "Транспорт", "description": "Поездка на такси"},
        {"date": "10.02.2023", "amount": 150.00, "category": "Еда", "description": "Заказ пиццы"}  # Исправленный ожидаемый результат
    ]
    assert result == expected_result


def test_search_transactions(sample_data):
    print(sample_data)  # Debug info
    result = search_transactions(sample_data, "еда")
    print(result)  # Debug info
    expected_len = 3
    assert len(result) == expected_len, f"Expected {expected_len}, but got {len(result)}"
    for item in result:
        assert 'еда' in item['Описание'].lower() or 'еда' in item['Категория'].lower()

# Запуск тестов
if __name__ == "__main__":
    pytest.main()