from sqlalchemy.orm import Session
from . import models
from app.schemas import user as user_schema
from app.schemas import message as message_schema

# --- User CRUD Functions ---

def get_all_users_for_admin(db: Session, skip: int = 0, limit: int = 100):
    """Fetches a paginated list of all users for an admin."""
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    """Fetches a user from the database by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: user_schema.UserCreate):
    """Creates a new user in the database."""
    db_user = models.User(
        email=user.email,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: models.User, user_in: user_schema.UserUpdate):
    """Updates a user's profile in the database."""
    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Message CRUD Functions ---

def create_message(db: Session, content: str, sender: str, owner_id: int):
    """Creates a new message in the database."""
    db_message = models.Message(
        content=content,
        sender=sender,
        owner_id=owner_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 30):
    """Fetches a paginated list of a user's ACTIVE messages (not deleted)."""
    return db.query(models.Message).filter(
        models.Message.owner_id == user_id,
        models.Message.is_deleted == False
    ).order_by(models.Message.timestamp.desc()).offset(skip).limit(limit).all()

def soft_delete_messages_by_user(db: Session, user_id: int):
    """Soft deletes all messages for a specific user by setting is_deleted = True."""
    db.query(models.Message).filter(
        models.Message.owner_id == user_id
    ).update({"is_deleted": True})
    db.commit()

# --- NEW Admin-Specific CRUD Functions ---

def get_deleted_messages_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 30):
    """Fetches a paginated list of a user's DELETED messages for an admin."""
    return db.query(models.Message).filter(
        models.Message.owner_id == user_id,
        models.Message.is_deleted == True
    ).order_by(models.Message.timestamp.desc()).offset(skip).limit(limit).all()

def get_all_messages_by_user_for_admin(db: Session, user_id: int, skip: int = 0, limit: int = 30):
    """Fetches a paginated list of ALL of a user's messages for an admin."""
    return db.query(models.Message).filter(
        models.Message.owner_id == user_id
    ).order_by(models.Message.timestamp.desc()).offset(skip).limit(limit).all()

