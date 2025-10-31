from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db import crud
from app.schemas.message import Message
from app.schemas.user import User
# Import our new api_key dependency
from app.security import api_key, jwt
from app.api.v1.auth import get_db

router = APIRouter()

@router.get(
    "/admin/users/",
    response_model=List[User],
    tags=["Admin"],
    dependencies=[Depends(api_key.get_api_key)]
)
def read_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    [SERVICE-TO-SERVICE ONLY] Retrieve a list of all users in the system.
    Requires a valid internal API key.
    """
    users = crud.get_all_users_for_admin(db, skip=skip, limit=limit)
    return users


@router.get(
    "/admin/users/{user_id}/history/all",
    response_model=List[Message],
    tags=["Admin"],
    # THIS IS THE CRITICAL CHANGE: Use the api_key dependency
    dependencies=[Depends(api_key.get_api_key)]
)
def read_all_user_history(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    [SERVICE-TO-SERVICE ONLY] Retrieve the complete chat history for a user.
    Requires a valid internal API key.
    """
    messages = crud.get_all_messages_by_user_for_admin(db, user_id=user_id, skip=skip, limit=limit)
    return messages


@router.get(
    "/admin/users/{user_id}/history/active",
    response_model=List[Message],
    tags=["Admin"],
    # UPDATED: This endpoint is now also protected by the internal API key.
    dependencies=[Depends(api_key.get_api_key)]
)
def read_active_user_history(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    [SERVICE-TO-SERVICE ONLY] Retrieve the active chat history for a specific user,
    excluding any messages they have cleared.
    """
    # We can reuse the standard user-facing function for this
    messages = crud.get_messages_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return messages


@router.get(
    "/admin/users/{user_id}/history/deleted",
    response_model=List[Message],
    tags=["Admin"],
    # UPDATED: This endpoint is now also protected by the internal API key.
    dependencies=[Depends(api_key.get_api_key)]
)
def read_deleted_user_history(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    [SERVICE-TO-SERVICE ONLY] Retrieve only the cleared (soft-deleted) chat history
    for a specific user.
    """
    messages = crud.get_deleted_messages_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return messages

