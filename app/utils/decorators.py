from typing import Callable
from functools import wraps
from fastapi import Request
from app.api.deps import get_user_address_from_cookie
from fastapi.exceptions import HTTPException


def check_user_auth(function: Callable):
    @wraps(function) # копирует имя, строку документации и сигнатуру исходной функции в обёртку
    def wrapper(*args, **kwargs):
        request = None
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break

        address = request.cookies.get("address")
        if request is None:
            # На всякий случай ищем в кваргах
            request = kwargs.get('request')        
        if address is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        return function(*args, **kwargs)
    return wrapper
    

