from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.eth.blockchain_gateway import factory_client

from app.utils.path import (
    TEMPLATE_PATH, 
    STATIC_PATH
)

templates = Jinja2Templates(directory=TEMPLATE_PATH)


app = FastAPI()

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )

