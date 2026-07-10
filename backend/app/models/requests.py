from backend.app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func
from backend.app.enums import AccountStatus, RequestStatus


class Request(Base):
    __tablename__ = "requests"

    request_id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    account_id : Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "accounts.account_id"
        ),
        nullable=False
    )

    request_from : Mapped[str] = mapped_column(SQLEnum(AccountStatus),nullable=False)
    request_to : Mapped[str] = mapped_column(SQLEnum(AccountStatus),nullable=False)
    request_status : Mapped[str] = mapped_column(SQLEnum(RequestStatus),nullable=False)
    date : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())