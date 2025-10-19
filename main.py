import logging

from src.utils import load_operations_df, load_user_settings
from src.views import build_main_response

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")

df = load_operations_df("data/operations.xlsx")
settings = load_user_settings("user_settings.json")
json_answer = build_main_response("2020-05-20 17:12:00", df, settings)
print(json_answer)
