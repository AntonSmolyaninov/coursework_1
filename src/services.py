import logging
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger(__name__)


def filter_df_by_month(df: pd.DataFrame, date_str: str) -> pd.DataFrame:
    """Фильтрует DataFrame по месяцу для заданной даты."""
    logger.info(f"Фильтрация операций по месяцу для даты {date_str}")
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    start = dt.replace(day=1, hour=0, minute=0, second=0)
    df = df.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    filtered = df[(df["Дата операции"] >= start) & (df["Дата операции"] <= dt)]
    logger.info(f"Отобрано операций за месяц: {len(filtered)}")
    return filtered


def get_card_spent(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Рассчитывает суммы расходов и кешбэка по картам на основе DataFrame."""
    logger.info("Расчет сумм расходов и кешбэка по картам")
    # Ключ - 4 цифры карты, значения - dict с last_digits, total_spent, cashback
    result: Dict[str, Dict[str, Any]] = {}
    for _, row in df.iterrows():
        card = str(row["Номер карты"])[-4:]
        amount = float(row["Сумма операции"])
        result.setdefault(card, {"last_digits": card, "total_spent": 0.0, "cashback": 0.0})
        if amount > 0:
            result[card]["total_spent"] += amount
            result[card]["cashback"] += amount / 100
    for card_info in result.values():
        card_info["total_spent"] = round(card_info["total_spent"], 2)
        card_info["cashback"] = round(card_info["cashback"], 2)
    logger.info(f"Обработано карт: {len(result)}")
    # Возвращаем список словарей с инфой по картам
    return sorted(result.values(), key=lambda x: x["total_spent"], reverse=True)


def get_top_transactions(df: pd.DataFrame, n: int = 5) -> List[Dict[str, Any]]:
    """Формирует топ-5 транзакций по сумме из DataFrame."""
    logger.info(f"Формируем топ-{n} транзакций по сумме")

    # Убедимся, что столбец "Дата операции" в формате datetime
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce", dayfirst=True)

    # Отбор топ-наиболее значимых транзакций
    df = df.sort_values("Сумма операции", ascending=False).head(n)
    logger.info(f"Топ-транзакций собрано: {len(df)}")

    # Заполняем список с необходимыми данными
    return [
        {
            "date": row["Дата операции"].strftime("%d.%m.%Y"),  # Преобразуем дату в строку
            "amount": round(row["Сумма операции"], 2),  # Округляем сумму до двух знаков
            "category": row["Категория"],  # Получаем категорию
            "description": row["Описание"],  # Получаем описание
        }
        for _, row in df.iterrows()
    ]


def search_transactions(df: pd.DataFrame, query: str) -> List[Dict[str, Any]]:
    """Возвращает все транзакции, содержащие 'query' (без учета регистра) в описании или категории."""
    logger.info(f"Выполняется поиск: '{query}'")

    # Приведение запроса к нижнему регистру
    q = query.lower()

    # Преобразование DataFrame в список словарей
    records = df.to_dict("records")

    # Фильтрация записей
    filtered = filter(
        lambda tx: q in str(tx.get("Описание", "")).lower() or q in str(tx.get("Категория", "")).lower(), records
    )

    # Преобразование фильтруемых записей обратно в список
    result: List[Dict[str, Any]] = list(filtered)
    logger.info(f"Найдено {len(result)} подходящих транзакций")

    return result
