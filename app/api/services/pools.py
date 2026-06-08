from app.models.pools import PoolAdresses
from fastapi.exceptions import HTTPException
from pathlib import Path

def get_pool_addresses(pool_path: Path) -> PoolAdresses:
    try:
        return PoolAdresses(
            ger_kre=pool_path["poolGerKre"],
            kre_rtk=pool_path["poolKreRtk"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to get pools: {str(e)}"
        )