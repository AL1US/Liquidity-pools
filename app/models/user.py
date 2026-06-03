from pydantic import BaseModel

class LoginRequest(BaseModel):
    public_key: str
