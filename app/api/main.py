from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.eth.blockchain_gateway import factory_client
from pydantic import BaseModel

import traceback

from app.utils.path import TEMPLATE_PATH, STATIC_PATH

class LoginRequest(BaseModel):
    public_key: str
    
app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
templates = Jinja2Templates(directory=TEMPLATE_PATH)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )
    
@app.post("/login")
async def login(request: Request, data: LoginRequest):
    user_address = data.public_key
    
    try:
        # Приводим адрес к правильному формату 
        checksum_address = factory_client.w3.to_checksum_address(user_address)
        
        # Call вызов
        user_data = factory_client.contract.functions.users(checksum_address).call()
        
        # На всякий случай делаем обработку и для того и для другого
        user_name = user_data[0] if isinstance(user_data, tuple) else user_data
        
        if not user_name:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Ваш адрес не зарегистрирован в системе смарт-контракта."}
            )
            
        return {"redirect": "/"}
        
    except Exception as e:
        # Мега обработчик от ии
        print(f"--- ОШИБКА БЛОКЧЕЙНА ---")
        traceback.print_exc()
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Ошибка сервера: {str(e)}"}
        )
        
@app.get("/api/pools")
async def get_pools():
    try:
        pools_addresses = factory_client.contract.functions.getPools().call()
        
        return {"pools": pools_addresses}
        
    except Exception as e:
        print(f"--- ОШИБКА ПРИ ПОЛУЧЕНИИ ПУЛОВ ---")
        traceback.print_exc()
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Ошибка сервера: {str(e)}"}
        )