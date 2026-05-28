from pathlib import Path
from config import ROOT_DIR
import json

# --- BLOCKCHAIN ----------
PROVIDER_URL = "http://127.0.0.1:8545"

BLOCKCHAIN_DIR = ROOT_DIR / "blockchain"
ARTIFACTS_DIR = BLOCKCHAIN_DIR / "artifacts/contracts"

# JSON CONTRACT PATHS
POOLS_JSON_PATH = ARTIFACTS_DIR / "Pools.sol" / "Pool.json" 
STAKING_JSON_PATH = ARTIFACTS_DIR / "Staking.sol" / "Staking.json" 
FACTORY_JSON_PATH = ARTIFACTS_DIR / "Factory.sol" / "Factory.json" 
ROUTER_JSON_PATH = ARTIFACTS_DIR / "Router.sol" / "Router.json" 
TOKEN_JSON_PATH = ARTIFACTS_DIR / "Token.sol" / "Token.json" 

# ADDRESSES
ADDRESSES_JSON_PATH = BLOCKCHAIN_DIR / "addresses/addresses.json"

try:
    with open(ADDRESSES_JSON_PATH, "r") as f:
       CONTRACT_ADDRESSES = json.load(f)
       
except FileNotFoundError as e:
    raise FileNotFoundError(
        f"Ошибка: Не удалось запустить модуль. Отсутствует файл конфигурации: {ADDRESSES_JSON_PATH.name}\n"
    ) from e
    
except json.JSONDecodeError as e:
    raise ValueError(f"Ошибка: Файл {ADDRESSES_JSON_PATH.name} содержит поврежденный JSON код!") from e
    
# --- FRONTEND PATHS ----------
STATIC_PATH = ROOT_DIR / "app" / "frontend" / "static"
 
TEMPLATE_PATH = ROOT_DIR / "app" / "frontend" / "templates"