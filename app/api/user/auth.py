import traceback

from fastapi import APIRouter, Form, Request, status, Response
from fastapi.responses import JSONResponse

from app.utils.frontend import templates
from app.classes.user import LoginRequest
from app.eth.blockchain_gateway import factory_client
    

router = APIRouter()

sessions = {}

@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth.html",
        context={"request": request}
    )

# апи для пост
@router.post("/login")
def login(request: Request, data: LoginRequest, response: Response):
    pk = data.public_key
    
    try:
        checksum_address = factory_client.w3.to_checksum_address(pk)

        user_data = factory_client.contract.functions.users(checksum_address).call()
         
        is_registered = user_data[0] if isinstance(user_data, tuple) else user_data
        
        if not is_registered:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Ваш адрес не зарегистрирован в системе смарт-контракта."}
            )

        response.set_cookie(key="address", value=checksum_address)

        return {"redirect": "/"}

    except Exception as e:
    # потом добавить логирование
        print("КАКАЯ ТО ОШИБКА ПРИ РЕГИСТРАЦИИ")
        traceback.print_exc()
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Ошибка сервера: {str(e)}"}
        )

# Выход
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("address")
    return {"redirect": "/login"}