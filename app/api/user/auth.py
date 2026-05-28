import traceback

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import JSONResponse

from app.utils.frontend import templates
from app.classes.user import LoginRequest
from app.eth.blockchain_gateway import factory_client

router = APIRouter()

@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth.html",
        context={"request": request}
    )

# апи для пост
@router.post("/login")
def login(request: Request, data: LoginRequest):
    pk = data.public_key
    
    try:
        checksum_address = factory_client.w3.to_checksum_address(pk)

        user_data = factory_client.contract.functions.users(checksum_address).call()
         
        user_name = pk[0] if isinstance(pk, tuple) else pk
        
        if not user_name:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Ваш адрес не зарегистрирован в системе смарт-контракта."}
            )
        
        return {"redirect": "/"}

    except Exception as e:
    # потом добавить логирование
        print("КАКАЯ ТО ОШИБКА ПРИ РЕГИСТРАЦИИ (ВХОД В АККАУНТ)")
        traceback.print_exc()
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Ошибка сервера: {str(e)}"}
        )
    
# принять данные

# вызвать метод регистрации если аккаунт не зареган 

# запомнить его в куках или в сессии

# вернуть ошибку или успех