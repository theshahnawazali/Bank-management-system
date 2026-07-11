import bcrypt
from datetime import datetime, timedelta
from jose import jwt, JWTError

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

SECRET_KEY = "Bank"
ALGORITHM = "HS256"

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

    except JWTError as e:
        raise ValueError("Invalid token")