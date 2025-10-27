# **Курсовой проект №1 по Python**
## Описание:
Приложение для анализа транзакций, которые находятся в Excel-файле.
Приложение генерирует JSON-данные для веб-страниц, формирует Excel-отчеты, 
а также предоставляет курсы валют, цены акций, отчеты по категориям за последние 3 месяца,
формирует топ-5 транзакций, расчитывает суммы расходов и кешбэка по картам.

## Описание функций:
1. `get_greeting` - Возвращает приветствие в зависимости от времени суток.
2. `build_main_response` - Формирует основной JSON-ответ для дашборда пользователя на заданную дату.
3. `load_operations_df`  - Загружает операции из Excel.
4. `load_user_settings` - Загружает словарь настроек пользователя
5. `filter_df_by_month` - Фильтрует DataFrame по месяцу для заданной даты.
6. `get_card_spent` - Рассчитывает суммы расходов и кешбэка по картам на основе DataFrame.
7. `get_top_transactions` - Формирует топ-5 транзакций по сумме из DataFrame.
8. `search_transactions` - Возвращает все транзакции, содержащие 'query' (без учета регистра) в описании или категории.
9. `get_currency_rates` - Получает курсы валют к рублю по списку currency_list (например ['USD', 'EUR']). Использует API Центробанка РФ.
10. `get_stock_prices` - Получает цены акций с помощью Alpha Vantage API. API-ключ берётся только из .env (переменная API_KEY_AV)
11. `save_report` - Декоратор для сохранения результата функции в JSON-файл.
12. `spending_by_category` - Функция — траты по категории.

## Установка:
1. Клонируйте репозиторий:
```https://github.com/AntonSmolyaninov/coursework_1```
2. Установите зависимости:
- `poetry init` — инициализировать пакет в существующем проекте.
- `poetry new package-name` — создать новый проект.
- `poetry install (dependency name)` — первичная установка.
- `poetry update` — обновление зависимостей.
- `poetry remove (dependency name)` — удалить зависимость из проекта.
- `poetry show--tree` — посмотреть всё дерево зависимостей.
- `poetry show --latest`— посмотреть, последние ли версии используются в проекте.
- `poetry install python-dotenv` - установка библиотеку dotenv.
- `poetry add requests` - установить библиотеку request.
- `poetry add pandas` - установка библиотеки pandas.

## Тестирование:
1. test_views.py - тестируем `build_main_response`
2. test_utils.py - тестируем `load_operations_df`, `load_user_settings`
3. test_services.py - тестируем `filter_df_by_month`, `get_card_spent`, `get_top_transactions`, `search_transactions`
4. test_reports.py - тестируем `spending_by_category`
5. test_market_apis.py - тестируем `get_currency_rates`, `get_stock_prices`

### Установка теста:
Установка через Poetry:
```poetry add --group dev pytest``` 
Установка pytest-cov:
```poetry add --group dev pytest-cov``` - Метрика, которая показывает, какой процент кода программы был протестирован.

## Запуск
`python3 main.py`

### Запуск тестов:
1. Запуск:
```pytest``` - запуск всех тестов.

2. Команды, чтобы запустить тесты с оценкой покрытия:
```pytest --cov``` — при активированном виртуальном окружении.
```poetry run pytest --cov``` — через poetry.
```pytest``` - запуск всех тестов.