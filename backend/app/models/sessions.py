from sqlalchemy import String, Integer, DateTime, Column, ForeignKey
from sqlalchemy.sql import func
from database.base import Base
from sqlalchemy import Enum as SQLEnum
from enums import SessionStatus


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True, index=True)

    chat_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    token = Column(String(255), unique=True, nullable=False)
    login_time = Column(DateTime(timezone=True), server_default=func.now())
    logout_time = Column(DateTime(timezone=True),nullable=True)
    status = Column(SQLEnum(SessionStatus),nullable=False)
    