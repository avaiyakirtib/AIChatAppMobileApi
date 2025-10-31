from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    """Base schema for a user, containing common attributes."""
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """Schema used when creating a new user."""
    pass

class UserUpdate(BaseModel):
    """Schema for updating a user's profile. All fields are optional."""
    full_name: Optional[str] = None
    username: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    theme_preference: Optional[str] = None

class User(UserBase):
    """Full user schema including database-generated and profile fields."""
    id: int
    is_active: bool
    username: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    theme_preference: Optional[str] = None

    class Config:
        """Pydantic configuration to allow ORM model mapping."""
        from_attributes = True

