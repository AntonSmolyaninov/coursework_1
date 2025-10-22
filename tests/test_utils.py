import pytest
import pandas as pd
from unittest import mock
import json
from src.utils import load_operations_df, load_user_settings


# Тест для функции load_operations_df
def test_load_operations_df(mocker):
    # Создаём фиктивный DataFrame для успешного теста
    mock_df = pd.DataFrame({
        'Номер карты': ['1234 5678 9012 3456'],
        'Дата операции': ['2023-10-05'],
        'Сумма операции': [1500],
        'Категория': ['Еда'],
        'Описание': ['Ужин в ресторане']
    })

    # Подменяем pd.read_excel, чтобы он вернул наш фиктивный DataFrame
    mocker.patch('pandas.read_excel', return_value=mock_df)

    # Запускаем функцию
    df = load_operations_df("mock_path.xlsx")

    # Проверяем результат
    assert len(df) == 1
    assert df['Номер карты'][0] == '1234 5678 9012 3456'


def test_load_operations_df_error(mocker):
    # Подменяем pd.read_excel, чтобы он вызвал ошибку
    mocker.patch('pandas.read_excel', side_effect=Exception("Ошибка загрузки"))

    # Пытаемся вызвать функцию и проверяем, что она вызывает исключение
    with pytest.raises(Exception):
        load_operations_df("wrong_path.xlsx")


# Тест для функции load_user_settings
def test_load_user_settings(mocker):
    # Создаём фиктивный словарь настроек
    mock_settings = {'theme': 'dark', 'language': 'en'}

    # Подменяем json.load, чтобы он вернул наш фиктивный словарь
    mocker.patch('builtins.open', mock.mock_open(read_data=json.dumps(mock_settings)))

    settings = load_user_settings("mock_settings.json")

    # Проверяем результат
    assert settings == mock_settings

def test_load_user_settings_error(mocker):
    # Подменяем open, чтобы он вызвал ошибку
    mocker.patch('builtins.open', side_effect=IOError("Ошибка чтения файла"))

    # Проверяем, что вызов функции вызывает исключение
    with pytest.raises(Exception):
        load_user_settings("wrong_path.json")
