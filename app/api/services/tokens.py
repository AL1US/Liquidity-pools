from fastapi.exceptions import HTTPException
from app.models.tokens import TokenAddresses
from pathlib import Path

def get_token_addresses(path_to_tokens: Path) -> TokenAddresses:
    try:
        return TokenAddresses(
            gerda=path_to_tokens["gerdaCoin"],
            krendel=path_to_tokens["krendelCoin"],
            rtk=path_to_tokens["rtkCoin"],
            professional=path_to_tokens["professionalCoin"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to get addresses: {str(e)}"
        )