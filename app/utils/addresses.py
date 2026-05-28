from app.utils.path import ADDRESSES_JSON_PATH
import json

try:
    with open(ADDRESSES_JSON_PATH, "r") as f:
       CONTRACT_ADDRESSES = json.load(f)
       
except FileNotFoundError as e:
    raise FileNotFoundError(
        f"Ошибка: Не удалось запустить модуль. Отсутствует файл конфигурации: {ADDRESSES_JSON_PATH.name}\n"
    ) from e
    
except json.JSONDecodeError as e:
    raise ValueError(f"Ошибка: Файл {ADDRESSES_JSON_PATH.name} содержит поврежденный JSON код!") from e