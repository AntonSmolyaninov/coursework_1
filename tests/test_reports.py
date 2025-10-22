import json
from unittest import mock

import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture
def transactions():
    return pd.DataFrame(
        {
            "date": ["2023-10-10", "2023-10-05", "2023-09-15", "2023-08-25"],
            "category": ["еда", "транспорт", "еда", "еда"],
            "amount": [150, 20, 100, 80],
        }
    )


# Тест для функции spending_by_category
def test_spending_by_category(transactions):
    result = spending_by_category(transactions, "еда", "2023-10-10")

    # Проверка результата
    assert len(result) == 3  # три трансакции в категории "еда" за последние 3 месяца
    assert all(result["category"].str.lower() == "еда")


# Тест для случая, когда ничего не найдено
def test_spending_by_category_empty(transactions):
    result = spending_by_category(transactions, "развлечения", "2023-10-10")

    # Проверка результата: ожидаем пустой DataFrame
    assert len(result) == 0


def test_save_report(mocker, transactions):
    # Заменяем open на mock, чтобы не сохранять файл
    mock_open = mock.mock_open()
    mocker.patch("builtins.open", mock_open)

    # Сохраним отчет
    result = spending_by_category(transactions, "еда", "2023-09-10")

    # Для проверки выведем что мы получили в result
    assert result is not None, "The result should not be None."

    # Проверяем, что результат не пустой
    assert not result.empty, "The result DataFrame should not be empty."

    # Проверяем, был ли вызван mock_open
    mock_open.assert_called_once()

    # Получаем имя файла
    output_filename = mock_open.call_args[0][0]

    # Проверяем, что имя файла содержит 'spending_by_category' и '.json'
    assert "spending_by_category" in output_filename
    assert output_filename.endswith(".json")

    # Проверяем, что содержимое файла соответствует ожидаемому результату
    expected_json = json.dumps(result.to_dict(orient="records"), ensure_ascii=False, indent=2)
    mock_open().write.assert_called_once_with(expected_json)
