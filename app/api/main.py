from fastapi import FastAPI, Request

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.utils.path import STATIC_PATH
from app.utils.frontend import templates

from app.eth.blockchain_gateway import factory_client
from app.api.user.auth import router as auth_router


app = FastAPI()

app.include_router(auth_router)

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )








