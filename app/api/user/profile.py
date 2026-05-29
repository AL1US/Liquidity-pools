from fastapi import APIRouter, Request

from app.utils.frontend import templates
from app.eth.blockchain_gateway import factory_client
from app.api.helpers import get_user_address

router = APIRouter()

@router.get("/profile")
