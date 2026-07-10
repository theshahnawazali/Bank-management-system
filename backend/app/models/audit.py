from backend.app.database.base import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, ForeignKey, String, DateTime
from backend.app.enums import UserRole, TransactionStatus
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func

class Audit(Base):
    __tablename__ = "auditlogs"

    log_id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id : Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "users.user_id"
        ),
        nullable=True
    )
    username : Mapped[str] = mapped_column(String(50),nullable=True)
    action : Mapped[str] = mapped_column(String(100),nullable=False)
    resource : Mapped[str] = mapped_column(String(15),nullable=False)
    ip_address : Mapped[str] = mapped_column(String(50),nullable=False)
    status : Mapped[SQLEnum] = mapped_column(SQLEnum(TransactionStatus), nullable=False)
    user_role : Mapped[SQLEnum] = mapped_column(String(10),nullable=True)
    description : Mapped[str] = mapped_column(String(255), nullable=False)
    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now())