from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.schemas.token import Token, GoogleToken, RefreshToken
from app.schemas.user import UserCreate
from app.security import sso, jwt
from app.db import crud
from app.db.session import SessionLocal
from app.services import redis_service

router = APIRouter()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/auth/google/signin", response_model=Token, tags=["Authentication"])
def google_signin(
    google_token: GoogleToken,
    db: Session = Depends(get_db)
):
    """
    Handles Google Sign-In.
    Verifies token, finds or creates a user, and returns access and refresh tokens.
    """
    user_info = sso.verify_google_token(google_token.token)
    if not user_info or not user_info.get("email"):
        raise HTTPException(status_code=400, detail="Invalid Google token payload")

    email = user_info["email"]
    db_user = crud.get_user_by_email(db, email=email)

    if not db_user:
        user_to_create = UserCreate(email=email, full_name=user_info.get("name"))
        db_user = crud.create_user(db, user=user_to_create)

    # Generate both tokens
    access_token = jwt.create_access_token(data={"sub": db_user.email})
    refresh_token = jwt.create_refresh_token(data={"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }

@router.post("/auth/refresh_token", response_model=Token, tags=["Authentication"])
def refresh_access_token(
    refresh_request: RefreshToken
):
    """
    Issues a new access token using a valid refresh token from the request body.
    """
    payload = jwt.verify_refresh_token_and_get_payload(refresh_request.refresh_token)
    
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token payload")

    new_access_token = jwt.create_access_token(data={"sub": email})
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "refresh_token": refresh_request.refresh_token # Pass back the same refresh token
    }


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT, tags=["Authentication"])
def logout(
    payload: dict = Depends(jwt.get_current_token_payload),
    token: str = Depends(jwt.oauth2_scheme)
):
    """
    Logs out the user by adding their access token to a denylist.
    """
    jti = payload.get("jti")
    exp = payload.get("exp")
    
    if not jti or not exp:
        raise HTTPException(status_code=400, detail="Invalid token for logout")

    time_now = datetime.now(timezone.utc).timestamp()
    expires_in = int(exp - time_now)

    if expires_in > 0:
        redis_service.add_token_to_denylist(jti, expires_in)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# @router.post("/auth/apple/signin", response_model=Token, tags=["Authentication"])
# def apple_signin(
#     apple_token: AppleToken,
#     db: Session = Depends(get_db)
# ):
#     user_info = sso.verify_apple_token(apple_token.identityToken)

#     if not user_info or not user_info.get("email"):
#         raise HTTPException(status_code=400, detail="Invalid Apple token payload")
    
#     email = user_info["email"]
#     db_user = crud.get_user_by_email(db, email=email)

#     if not db_user:
#         if not apple_token.fullName:
#             raise HTTPException(status_code=400, detail="Full name is required for new Apple users")
        
#         user_to_create = UserCreate(
#             email=email,
#             full_name=apple_token.fullName
#         )
#         db_user = crud.create_user(db, user=user_to_create)

#     token_data = {"sub": db_user.email}
#     return {
#         "access_token": jwt.create_access_token(data=token_data),
#         "refresh_token": jwt.create_refresh_token(data=token_data),
#         "token_type": "bearer",
#     }

