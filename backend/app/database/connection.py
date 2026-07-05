from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)