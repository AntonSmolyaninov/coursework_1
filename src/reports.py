import json
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional, Union  # Не забудь импортировать Any

import pandas as pd

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Декоратор для сохранения отчетов в файл
def save_report(func: Optional[Callable] = None, filename: Optional[str] = None) -> Callable:
    """Декоратор для сохранения результата функции в JSON-файл.
    Если не указан `filename`, имя файла будет сформировано автоматически на основе имени функции
    и текущей даты/времени."""

    def decorator(inner_func: Callable) -> Callable:
        @wraps(inner_func)
        def wrapper(*args: Any, **kwargs: Any) -> Union[pd.DataFrame, Any]:
            result = inner_func(*args, **kwargs)
            output_filename = filename
            if not output_filename:
                output_filename = f"{inner_func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            # Логирование результата перед записью
            logger.info(f"Result for {inner_func.__name__}: {result}")

            with open(output_filename, "w", encoding="utf-8") as f:
                # Преобразование результата в JSON строку
                if isinstance(result, pd.DataFrame) and not result.empty:
                    json_string = json.dumps(result.to_dict(orient="records"), ensure_ascii=False, indent=2)
                    f.write(json_string)  # Пишем в файл все за один раз
                else:
                    logger.warning("The result is not a DataFrame or is empty, not saving to file.")
                    f.write("[]")  # Записываем пустой список

            logger.info(f"Отчёт записан в: {output_filename}")
            return result

        return wrapper

    if func and callable(func):
        return decorator(func)
    return decorator


# Функция — траты по категории
@save_report
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает DataFrame с тратами по выбранной категории за последние 3 месяца.
    """
    logger.info(f"start, category='{category}', date='{date}'")

    # Приведение date к datetime
    if date:
        try:
            dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt = datetime.strptime(date, "%Y-%m-%d")
    else:
        dt = datetime.now()

    three_months_ago = dt - timedelta(days=90)

    df = transactions.copy()
    df["date"] = pd.to_datetime(df["date"])
    result = df[
        (df["category"].str.lower() == category.lower()) & (df["date"] >= three_months_ago) & (df["date"] <= dt)
    ]

    # Логирование количества найденных строк
    logger.info(f"rows found: {len(result)}")

    # Преобразуем дату в строку, если результат не пустой
    if not result.empty:
        result["date"] = result["date"].dt.strftime("%Y-%m-%d")  # Преобразование даты в строку

    return result
