import bcrypt
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.responses import JSONResponse
import random
from backend.app.database.connection import redis_conn
from backend.app.core.config import ALGORITHM, SECRET_KEY

def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

def verify_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )

def create_session_token(
    data : dict # Username and role -> Token
) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    payload.update({"exp" : expire})

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token

def verify_session_token(
    token : str
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload
    
    except ExpiredSignatureError as e:
        raise ValueError("Token has expired")
    
    except JWTError as e:
        raise ValueError("Invalid token")
    
    
def generete_random_otp(
    username : str
):
    key = f'{username}:otp'
    
    otp = random.randint(100000, 999999)

    redis_conn.set(key, otp, 600)

    return True