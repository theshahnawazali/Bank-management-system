import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import (
    REDIS_HOSTNAME,
    REDIS_PORT,
    REDIS_USERNAME,
    REDIS_PASSWORD,
    MYSQL_USERNAME,
    MYSQL_DATABASE_NAME,
    MYSQL_HOSTNAME,
    MYSQL_PASSWORD,
    DATABASE_URL
)


# engine = create_engine(f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE_NAME}", echo=False)
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

redis_conn = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)