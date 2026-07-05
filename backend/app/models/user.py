from database.base import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable= False)
    password = Column(String(255), unique=False, nullable=False)
    role = Column(String(20), default="customer")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
