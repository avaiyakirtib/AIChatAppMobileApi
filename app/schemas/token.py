from pydantic import BaseModel

class AccessToken(BaseModel):
    """Schema for returning just an access token."""
    access_token: str
    token_type: str = "bearer"

class Token(AccessToken):
    """Schema for returning both access and refresh tokens."""
    refresh_token: str

class TokenData(BaseModel):
    email: str | None = None

class GoogleToken(BaseModel):
    token: str

class AppleToken(BaseModel):
    token: str
    full_name: str | None = None

class RefreshToken(BaseModel):
    refresh_token: str

