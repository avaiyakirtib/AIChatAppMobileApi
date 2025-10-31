from fastapi import HTTPException, status
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import jwt # PyJWT library for Apple
import requests # For fetching Apple's public keys

from app.core.config import settings

# --- Google Verification ---
def verify_google_token(token: str) -> dict:
    """
    Verifies the Google ID token against a list of allowed client IDs.
    """
    try:
        # Pass the entire list of client IDs for verification.
        # The library will succeed if the token's audience matches ANY of them.
        id_info = id_token.verify_oauth2_token(
            token, google_requests.Request(), settings.GOOGLE_CLIENT_IDS
        )
        return id_info
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate Google credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

# --- Apple Verification ---
APPLE_PUBLIC_KEYS = None

def get_apple_public_keys() -> dict:
    """
    Fetches Apple's public keys for token verification.
    Includes a simple in-memory cache to avoid repeated network calls.
    """
    global APPLE_PUBLIC_KEYS
    if APPLE_PUBLIC_KEYS is None:
        try:
            response = requests.get("https://appleid.apple.com/auth/keys")
            response.raise_for_status()
            APPLE_PUBLIC_KEYS = response.json()["keys"]
        except requests.RequestException:
            raise HTTPException(status_code=500, detail="Could not fetch Apple public keys")
    return APPLE_PUBLIC_KEYS

def verify_apple_token(token: str) -> dict:
    """
    Verifies the Apple ID token ('identityToken' from the frontend).
    """
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        if not kid:
            raise ValueError("Key ID (kid) not found in token header")

        keys = get_apple_public_keys()
        matching_key = next((key for key in keys if key["kid"] == kid), None)
        if not matching_key:
            raise ValueError("Matching public key not found for the given Key ID")

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(matching_key)

        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=settings.APPLE_BUNDLE_ID,
            issuer="https://appleid.apple.com"
        )
        return payload
    except (jwt.PyJWTError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate Apple credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

