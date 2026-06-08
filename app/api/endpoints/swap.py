from fastapi import APIRouter, Request, Depends
from app.api.deps import get_current_address
from app.utils.frontend import templates
from app.utils.addresses import CONTRACT_ADDRESSES
from app.api.services.pools import get_pool_addresses
from app.api.services.tokens import get_token_addresses
router = APIRouter()

@router.get("/swap")
def swap(request: Request, address: str = Depends(get_current_address)):

    pools = get_pool_addresses(CONTRACT_ADDRESSES["pools"])
    tokens = get_token_addresses(CONTRACT_ADDRESSES["tokens"])

    return templates.TemplateResponse(
        request=request,
        name="swap.html",
        context={
            "request": request,
            **pools.model_dump(),
            **tokens.model_dump()
        }
    )

# router.post("/swap")
# def swap(request: Request, address: str = Depends(get_current_address)):
    
    
#     # understand wich pool
    
#     # transact witch this pool
    
#     # And exceptions and return
    
    
    
    
