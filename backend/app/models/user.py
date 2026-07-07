from database.base import Base
from enums import UserRole
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    user_id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name : Mapped[str] = mapped_column(String(50), nullable=False)
    username : Mapped[int] = mapped_column(String(50), unique=True, nullable=False)
    email : Mapped[str] = mapped_column(String(100),unique=True, nullable=False)
    password : Mapped[str] = mapped_column(String(100),nullable=False)
    role : Mapped[str] = mapped_column(Enum(UserRole), nullable=False)
    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now()) 
