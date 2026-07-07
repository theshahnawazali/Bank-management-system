from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, Float, Column, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy import Enum as SQLEnum
from database.base import Base
from enums import TransactionStatus, TransactionType


class Transaction(Base):
    __tablename__ = "transactions"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    account_id : Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "accounts.account_id"
        ),
        nullable=False
    )

    amount : Mapped[float] = mapped_column(Float,nullable=False)
    transaction_id : Mapped[str] = mapped_column(String(255),nullable=False)
    transaction_type : Mapped[str] = mapped_column(SQLEnum(TransactionType),nullable=False)
    date : Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    status : Mapped[str] = mapped_column(SQLEnum(TransactionStatus),nullable=False)
    description : Mapped[str] = mapped_column(String(255),nullable=True)