from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from app.utils.frontend import templates
from app.api.services.balance import get_balances

from app.api.deps import get_current_address

router = APIRouter()

@router.get("/profile")
def profile(request: Request, address: str = Depends(get_current_address)):

    balances = get_balances(address)
    
    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "request": request,
            **balances.model_dump() # ** распаковывает словарь. model_dump - штука из pydantic, которая возрващает словарь из полей модели
        }
    )

