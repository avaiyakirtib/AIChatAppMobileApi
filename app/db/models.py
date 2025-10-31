from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

# Create a base class for our models to inherit from
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True) # For potential future email/password auth
    is_active = Column(Boolean, default=True)
    
    # NEW: Add the admin flag
    is_admin = Column(Boolean, default=False, nullable=False)

    # Profile fields
    username = Column(String, unique=True, index=True, nullable=True)
    gender = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    theme_preference = Column(String, default="light")

    # Relationship to messages
    messages = relationship("Message", back_populates="owner", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    sender = Column(String, nullable=False) # 'user' or 'agent'
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_deleted = Column(Boolean, default=False, nullable=False)

    # Relationship to user
    owner = relationship("User", back_populates="messages")

