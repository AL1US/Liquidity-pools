from app.blockchain.clients import (
    gerda_client,
    krendel_client,
    rtk_client,
    professional_client
)
from fastapi.exceptions import HTTPException
from app.models.tokens import TokenBalances
from asyncio import gather # Для паралельного запуска нескольких асинхронных задач и сбора их результатов

async def get_balances(address: str) -> TokenBalances:
    try:
        
        gerda, krendel, rtk, professional = await gather(
                gerda_client.contract.functions.balanceOf(address).call(),
                krendel_client.contract.functions.balanceOf(address).call(),
                rtk_client.contract.functions.balanceOf(address).call(),
                professional_client.contract.functions.balanceOf(address).call(),
            )
        
        return TokenBalances(
            gerda=gerda,
            krendel=krendel,
            rtk=rtk,
            professional=professional,
        )

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to get balances: {str(e)}"
        )

