from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = "mysql+pymysql://root:password@localhost/Bankdb"

DAILY_LIMIT = 20000

MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_HOSTNAME = os.environ.get("MYSQL_HOSTNAME")
MYSQL_DATABASE_NAME = os.environ.get("MYSQL_HOSTNAME")

REDIS_HOSTNAME = os.environ.get("REDIS_HOSTNAME")
REDIS_PORT = os.environ.get("REDIS_USERNAME")
REDIS_USERNAME = os.environ.get("REDIS_USERNAME")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")


SECRET_KEY = "Bank"
ALGORITHM = "HS256"