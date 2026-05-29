from fastapi import Request


# Проверка сессии
def get_user_address(request: Request):
    return request.cookies.get("address")
