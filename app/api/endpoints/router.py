from fastapi import APIRouter, Form, Depends
from fastapi.exceptions import HTTPException
from app.api.deps import get_current_address
from app.utils.tokens import TOKEN_MAPPING
from app.blockchain.clients import router_client
from app.utils.addresses import CONTRACT_ADDRESSES

middle_token = CONTRACT_ADDRESSES["tokens"]["krendelCoin"]

router = APIRouter()

@router.post("/router_swap")
def router_swap(
        address: str = Depends(get_current_address), # От кого выполняем
        token_in: str = Form(...), 
        token_out: str = Form(...),
        amount: int = Form(...)
    ):
    try:
        token_client = TOKEN_MAPPING.get(token_in.lower())
        token_client.contract.functions.approve(router_client.contract.address, 2**256 - 1).transact({"from": address})
        router_client.contract.functions.swapTwoPools(token_in, middle_token, token_out, amount).transact({"from": address})
        return {"status": "success", "message": "Транзакция выполнена успешно"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")
