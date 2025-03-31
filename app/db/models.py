from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .db import Base
import enum

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    input = Column(String)
    model_rating = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Define the relationship to the User model
    user = relationship("User", back_populates="prompts")

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.USER)

    # Define the relationship to the Prompt model
    prompts = relationship("Prompt", order_by=Prompt.id, back_populates="user", cascade="all, delete-orphan")
