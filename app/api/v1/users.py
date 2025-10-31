from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import user as user_schema
from app.db import crud, models
from app.security import jwt
from app.db.session import SessionLocal

router = APIRouter()

# Dependency to get a DB session - THIS IS THE FIX
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users/me", response_model=user_schema.User, tags=["Users"])
def read_users_me(
    current_user: models.User = Depends(jwt.get_current_user),
    token: str = Depends(jwt.oauth2_scheme) # For Swagger UI
):
    """
    Fetch the profile for the currently authenticated user.
    """
    return current_user


@router.patch("/users/me", response_model=user_schema.User, tags=["Users"])
def update_users_me(
    user_update: user_schema.UserUpdate,
    payload: dict = Depends(jwt.get_current_token_payload), # Get payload to fetch user with the right session
    db: Session = Depends(get_db), # Use the local get_db
    token: str = Depends(jwt.oauth2_scheme) # For Swagger UI
):
    """
    Update the authenticated user's profile.
    """
    email = payload.get("sub")
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return crud.update_user(db=db, db_user=db_user, user_in=user_update)

