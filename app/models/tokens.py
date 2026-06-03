from pydantic import BaseModel

class TokenBalances(BaseModel):
    gerda: int 
    krendel: int
    rtk: int
    professional: int