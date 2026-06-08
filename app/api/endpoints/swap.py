from fastapi import APIRouter, Form, Request, Depends
from fastapi.exceptions import HTTPException
from app.api.deps import get_current_address, get_pool_client
from app.utils.frontend import templates
from app.utils.addresses import CONTRACT_ADDRESSES
from app.api.services.tokens import get_token_addresses
from app.utils.tokens import TOKEN_MAPPING

from app.blockchain.clients import poolGerKre_client, poolKreRtk_client

from app.blockchain.blockchain_gateway import BaseContractClient
router = APIRouter()

@router.get("/swap")
def swap(request: Request, address: str = Depends(get_current_address)):

    tokens = get_token_addresses(CONTRACT_ADDRESSES["tokens"])

    return templates.TemplateResponse(
        request=request,
        name="swap.html",
        # Очень ужасно передаётся, по хорошему где то записать 1 объект и потом его просто распоковать
        context={
            "request": request,
            **tokens.model_dump(),
            "ger_kre": poolGerKre_client,
            "kre_rtk": poolKreRtk_client,
        }
    )

@router.post("/swap")
def swap_post(
        request: Request,
        address: str = Depends(get_current_address), # От кого выполняем
        pool_client: BaseContractClient = Depends(get_pool_client), # Клиент для транзакци
        token: str = Form(...), # адрес для транзакции
        amount: int = Form(...)
    ):
    try:
        token_client = TOKEN_MAPPING.get(token.lower())
        token_client.contract.functions.approve(pool_client.contract.address, 2**256 - 1).transact({"from": address})
        pool_client.contract.functions.swap_token(token, amount).transact({"from": address})
        return {"status": "success", "message": "Транзакция выполнена успешно"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")
