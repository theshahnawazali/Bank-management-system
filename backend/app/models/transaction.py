from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, Float, Column, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy import Enum as SQLEnum
from database.base import Base
from enums import TransactionStatus, TransactionType


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=False
    )

    amount = Column(Float, nullable=False)
    transaction_id = Column(String(100), nullable=False, unique=True)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(SQLEnum(TransactionStatus), nullable=False)
    description = Column(String(255), nullable=True)
