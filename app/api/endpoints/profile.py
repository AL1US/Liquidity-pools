from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.utils.frontend import templates
from app.blockchain.clients import (
    gerda_client,
    krendel_client,
    rtk_client,
    professional_client
)

from app.api.deps import get_user_address_from_cookie

router = APIRouter()

@router.get("/profile")
def profile(request: Request):
    # проверка на то зареган ли человек
    pk = get_user_address_from_cookie(request)
    
    if pk == "":
        return RedirectResponse(url="/login", status_code=302)

    gerda = gerda_client.contract.functions.balanceOf(pk).call()
    krendel = krendel_client.contract.functions.balanceOf(pk).call()
    rtk = rtk_client.contract.functions.balanceOf(pk).call()
    professional = professional_client.contract.functions.balanceOf(pk).call()
    
    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "request": request,
            "gerda": gerda,
            "krendel": krendel,
            "rtk": rtk,
            "professional": professional
        }
    )
    