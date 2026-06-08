from fastapi import APIRouter, Form, Request, Depends
from fastapi.exceptions import HTTPException
from app.api.deps import get_current_address, get_pool_client
from app.utils.frontend import templates
from app.utils.addresses import CONTRACT_ADDRESSES
from app.api.services.tokens import get_token_addresses
from app.utils.tokens import TOKEN_MAPPING

from app.blockchain.clients import poolGerKre_client, poolKreRtk_client, staking_client

from app.blockchain.blockchain_gateway import BaseContractClient
router = APIRouter()

@router.get("/investions")
def investions(request: Request, address: str = Depends(get_current_address)):

    tokens = get_token_addresses(CONTRACT_ADDRESSES["tokens"])
    reward = staking_client.contract.functions.calculateReward().call({"from": address})

    return templates.TemplateResponse(
        request=request,
        name="investions.html",
        # Очень ужасно передаётся, по хорошему где то записать 1 объект и потом его просто распоковать
        context={
            "request": request,
            **tokens.model_dump(),
            "ger_kre": poolGerKre_client,
            "kre_rtk": poolKreRtk_client,
            "reward": reward
        }
    )

@router.post("/liquidity_up")
def liquidity_up(
        address: str = Depends(get_current_address), # От кого выполняем
        pool_client: BaseContractClient = Depends(get_pool_client), # Клиент для транзакци
        token: str = Form(...), # адрес для транзакции
        amount: int = Form(...)
    ):
    try:
        token_client = TOKEN_MAPPING.get(token.lower())
        token_client.contract.functions.approve(pool_client.contract.address, 2**256 - 1).transact({"from": address})
        pool_client.contract.functions.liquidityUp(token, amount).transact({"from": address})
        return {"status": "success", "message": "Транзакция выполнена успешно"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")


@router.post("/stake")
def stake(
        address: str = Depends(get_current_address), # От кого выполняем
        token: str = Form(...),
        amount: int = Form(...)
    ):
    try:
        token_client = TOKEN_MAPPING.get(token.lower())
        token_client.contract.functions.approve(staking_client.contract.address, 2**256 - 1).transact({"from": address})
        staking_client.contract.functions.stake(amount).transact({"from": address})
        return {"status": "success", "message": "Транзакция выполнена успешно"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")

@router.post("/claim_reward")
def claim_reward(
        address: str = Depends(get_current_address),
    ):
    try:
        staking_client.contract.functions.claimReward().transact({"from": address})
        return {"status": "success", "message": "Транзакция выполнена успешно"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")