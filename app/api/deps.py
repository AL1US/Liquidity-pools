from fastapi import Request, Form
from fastapi import HTTPException
from app.blockchain.blockchain_gateway import BaseContractClient
from app.utils.pools import POOL_DICT
from app.utils.tokens import TOKEN_DICT

# Проверка сессии
def get_current_address(request: Request) -> str:
    addr = request.cookies.get("address")
    if addr is None:
        raise HTTPException(401, "Not authenticated")
    return addr

# Получение клиента пула
def get_pool_client(pool_id: str = Form(...)) -> BaseContractClient:
    client = POOL_DICT.get(pool_id)
    if not client:
        raise HTTPException(status_code=400, detail="Unknown pool ID")
    return client

# Получение клиента токена
def get_token_client(token_id: str = Form(...)) -> BaseContractClient:
    client = TOKEN_DICT.get(token_id)
    if not client:
        raise HTTPException(status_code=400, detail="Unknown pool ID")
    return client