from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from database.base import Base
from sqlalchemy import Enum as SQLEnum
from enums import SessionStatus


class Session(Base):
    __tablename__ = "sessions"

    session_id : Mapped[int] = mapped_column(Integer, primary_key=True,index=True)

    chat_id : Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "users.user_id"
        ),
        nullable=False
    )
    
    token : Mapped[str] = mapped_column(String(255),nullable=False,unique=True)
    login_time : Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    logout_time : Mapped[DateTime] = mapped_column(DateTime(timezone=True),nullable=True)
    status : Mapped[str] = mapped_column(SQLEnum(SessionStatus),nullable=False)
    