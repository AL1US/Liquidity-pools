from pydantic import BaseModel

class TokenBalances(BaseModel):
    gerda: int 
    krendel: int
    rtk: int
    professional: int
    
class TokenAddresses(BaseModel):
    gerda: str 
    krendel: str
    rtk: str
    professional: str