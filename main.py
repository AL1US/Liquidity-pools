from fastapi import FastAPI, Request

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.utils.path import STATIC_PATH
from app.utils.frontend import templates

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.profile import router as profile_router
from app.api.endpoints.swap import router as swap_router

from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(swap_router)

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        # Your OpenAPI document
        openapi_url=app.openapi_url,
        # Avoid CORS issues (optional)
        scalar_proxy_url="https://proxy.scalar.com",
    )





