from fastapi import APIRouter, Form, Request, Depends
from fastapi.exceptions import HTTPException
from app.api.deps import get_current_address, get_pool_client, get_token_client
from app.utils.frontend import templates
from app.utils.addresses import CONTRACT_ADDRESSES
from app.api.services.pools import get_pool_addresses
from app.api.services.tokens import get_token_addresses

from app.blockchain.clients import poolGerKre_client, poolKreRtk_client

from app.blockchain.clients import (
    gerda_client,
    krendel_client,
    rtk_client,
    professional_client
)

from app.blockchain.blockchain_gateway import BaseContractClient
router = APIRouter()

@router.get("/swap")
def swap(request: Request, address: str = Depends(get_current_address)):

    pools = get_pool_addresses(CONTRACT_ADDRESSES["pools"])
    tokens = get_token_addresses(CONTRACT_ADDRESSES["tokens"])

    return templates.TemplateResponse(
        request=request,
        name="swap.html",
        # Очень ужасно передаётся, по хорошему где то записать 1 объект и потом его просто распоковать
        context={
            "request": request,
            **pools.model_dump(),
            **tokens.model_dump(),
            "ger_kre": poolGerKre_client,
            "kre_rtk": poolKreRtk_client,
            "gerda_client": gerda_client,
            "krendel_client": krendel_client,
            "rtk_client": rtk_client,
            "professional_client": professional_client
        }
    )

@router.post("/swap")
def swap_post(
        request: Request,
        address: str = Depends(get_current_address),
        token_client: BaseContractClient = Depends(get_token_client),
        pool_client: BaseContractClient = Depends(get_pool_client),
        token: str = Form(...), # адрес для транзакции
        amount: int = Form(...)
    ):
    try:
        
        pool_client.contract.functions.swap_token(token, amount).transact({"from": address})
        return {"status": "success", "message": "Транзакция выполнена успешно"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")
