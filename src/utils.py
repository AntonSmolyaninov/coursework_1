import json
import logging
from typing import Any, Dict

import pandas as pd

logger = logging.getLogger(__name__)


def load_operations_df(path: str) -> pd.DataFrame:
    """Загружает операции из Excel"""
    logger.info(f"Чтение Excel-файла операций: {path}")
    try:
        df = pd.read_excel(path, sheet_name="Отчет по операциям")
        logger.info(f"Успешно загружено операций: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Ошибка при загрузке Excel-файла: {e}")
        raise


def load_user_settings(path: str = "user_settings.json") -> Dict[str, Any]:
    """Загружает словарь настроек пользователя"""
    logger.info(f"Чтение настроек пользователя из {path}")
    try:
        with open(path, encoding="utf-8") as f:
            settings: Dict[str, Any] = json.load(f)
        logger.info("Настройки пользователя загружены")
        return settings
    except Exception as e:
        logger.error(f"Ошибка при чтении user_settings.json: {e}")
        raise
