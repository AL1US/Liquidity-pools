from fastapi.templating import Jinja2Templates
from app.utils.path import TEMPLATE_PATH

templates = Jinja2Templates(directory=TEMPLATE_PATH)