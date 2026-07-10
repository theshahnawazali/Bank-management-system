from sqlalchemy import Float, DateTime, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func
from backend.app.database.base import Base
from backend.app.enums import AccountType, AccountStatus

class Account(Base):
    __tablename__ = "accounts"

    account_id : Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    
    user_id : Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "users.user_id"
        ),
        nullable=False
    )
    
    account_number : Mapped[int] = mapped_column(BigInteger,unique=True,nullable=False)
    account_type : Mapped[str] = mapped_column(SQLEnum(AccountType),nullable=False)
    balance : Mapped[float] = mapped_column(Float, nullable=False)
    status : Mapped[str] = mapped_column(SQLEnum(AccountStatus),nullable=False)
    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
