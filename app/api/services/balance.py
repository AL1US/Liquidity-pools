from app.blockchain.clients import (
    gerda_client,
    krendel_client,
    rtk_client,
    professional_client
)
from fastapi.exceptions import HTTPException
from app.models.tokens import TokenBalances

def get_balances(address: str) -> TokenBalances:
    try:
        return TokenBalances(
            gerda=gerda_client.contract.functions.balanceOf(address).call(),
            krendel=krendel_client.contract.functions.balanceOf(address).call(),
            rtk=rtk_client.contract.functions.balanceOf(address).call(),
            professional=professional_client.contract.functions.balanceOf(address).call(),
        )

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed ro get balances: {str(e)}"
        )