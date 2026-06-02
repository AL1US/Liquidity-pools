from fastapi import Request
from typing import Optional

# Проверка сессии
def get_user_address_from_cookie(request: Request) -> Optional[str]:
    return request.cookies.get("address")
