from fastapi import Request
from fastapi import Depends
from typing import Optional
from fastapi import HTTPException


# Проверка сессии
def get_current_address(request: Request) -> str:
    addr = request.cookies.get("address")
    if addr is None:
        raise HTTPException(401, "Not authenticated")
    return addr
