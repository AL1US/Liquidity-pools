from fastapi import APIRouter, Request, Depends
from app.api.deps import get_current_address
from app.utils.frontend import templates

router = APIRouter()

@router.get("/swap")
def swap(request: Request, address: str = Depends(get_current_address)):

    return templates.TemplateResponse(
        request=request,
        name="swap.html",
        context={"request": request}
    )
