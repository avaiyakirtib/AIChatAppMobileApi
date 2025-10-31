from pydantic import BaseModel
from datetime import datetime

# --- Schemas for the API ---

class PromptRequest(BaseModel):
    """Schema for the user's incoming prompt."""
    prompt: str

class PromptResponse(BaseModel):
    """Schema for the agent's outgoing answer."""
    answer: str

# --- Base Schema for Database Operations ---

class MessageBase(BaseModel):
    """Base schema for a message, containing all common fields."""
    content: str
    sender: str # "user" or "agent"

class MessageCreate(MessageBase):
    """Schema used when creating a new message in the database."""
    pass

# --- Full Schema for API Responses ---

class Message(MessageBase):
    """
    Full message schema for returning data through the API.
    Includes database-generated fields.
    """
    id: int
    owner_id: int
    timestamp: datetime
    is_deleted: bool  # <-- THIS IS THE NEW, IMPORTANT FIELD

    class Config:
        """Pydantic configuration to allow ORM model mapping."""
        from_attributes = True

