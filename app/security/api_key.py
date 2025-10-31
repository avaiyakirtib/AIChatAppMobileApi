from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

# Define the name of the custom header we will look for
API_KEY_NAME = "X-Internal-API-Key"

# Create the security scheme
api_key_header_scheme = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header_scheme)):
    """
    Dependency that checks for a valid internal API key in the request header.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="An internal API key is required for this operation.",
        )
    if api_key == settings.TRUSTED_ADMIN_API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid internal API key.",
        )

