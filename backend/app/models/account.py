from sqlalchemy import Column, String, Float, DateTime, Integer, BigInteger, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func
from database.base import Base
from database.connection import engine
from enums import AccountType, AccountStatus

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    account_number = Column(BigInteger, unique=True, nullable=False)
    account_type = Column(SQLEnum(AccountType), nullable=False)
    balance = Column(Float, nullable=False)
    status = Column(SQLEnum(AccountStatus), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    