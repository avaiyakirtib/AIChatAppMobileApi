from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import crud
from app.db.models import User
from app.schemas.message import PromptRequest, PromptResponse, Message
from app.security import jwt
from app.api.v1.auth import get_db

router = APIRouter()


@router.post("/chat/prompt", response_model=PromptResponse, tags=["Chat"])
def get_chat_response(
    request: PromptRequest,
    current_user: User = Depends(jwt.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Receives a user prompt, gets a dummy response, and saves both to the
    conversation history.
    """
    # This is a placeholder for the real AI agent call
    # For now, it just echoes the user's name and prompt
    from app.services import prompt_builder
    from app.agents import dummy_agent

    system_prompt = prompt_builder.build_prompt(
        template_name="main_system_prompt",
        user=current_user
    )
    
    ai_response = dummy_agent.get_dummy_response(
        system_prompt=system_prompt,
        user_prompt=request.prompt
    )

    # --- THIS IS THE FIX ---
    # Call create_message with the correct keyword arguments: content, sender, owner_id

    # Save user's prompt to DB
    crud.create_message(
        db=db,
        content=request.prompt,
        sender="user",
        owner_id=current_user.id
    )

    # Save agent's response to DB
    crud.create_message(
        db=db,
        content=ai_response,
        sender="agent",
        owner_id=current_user.id
    )

    return PromptResponse(answer=ai_response)


@router.get("/chat/history", response_model=List[Message], tags=["Chat"])
def get_chat_history(
    skip: int = 0,
    limit: int = 30,
    current_user: User = Depends(jwt.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves the paginated chat history for the authenticated user.
    """
    messages = crud.get_messages_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return messages


@router.post("/chat/clear", status_code=status.HTTP_200_OK, tags=["Chat"])
def clear_chat_history(
    current_user: User = Depends(jwt.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Soft deletes the entire chat history for the authenticated user.
    """
    crud.soft_delete_messages_by_user(db, user_id=current_user.id)
    return {"status": "success", "message": "Chat history has been successfully cleared."}


@router.get("/chat/status", tags=["Chat"])
def get_user_status(current_user: User = Depends(jwt.get_current_user)):
    """
    A simple endpoint to check if the user's token is valid (i.e., they are 'online').
    """
    return {"status": "online"}