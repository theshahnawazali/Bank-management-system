import redis
from database.connection import SessionLocal
from models.user import User
from database.connection import redis_conn
from utils.security import hash_password, verify_password, generate_session_token
from utils.id_generator import generate_token
from sqlalchemy import select
from utils.id_generator import generate_otp

db = SessionLocal() # Will be removed when include fast api

class AuthService:
    @classmethod
    def register(
        cls,
        name : str,
        email : str,
        username : str,
        password : str,
        role : str = "Customer"
        # db 
    ):
        UserEmail = db.query(User).filter(User.email == email).first()
        UserUsername = db.query(User).filter(User.username == username).first()

        # Check unique Email
        if UserEmail:
            return {
                "status" : False,
                "message" : "Email already exits.",
                "role" : None
            }
        
        else:
            # Check Unique Username
            if UserUsername:
                return {
                    "status" : False,
                    "message" : "Username already exits.",
                    "role" : None
                }
            
            else:
                if cls.set_session_token(username, role):
                    redis_conn.hset(
                        f"user:{username}",
                        mapping={
                            "name" : name,
                            "username" : username,
                            "email" : email,
                            "password" : hash_password(password),
                            "role" : role
                        }
                    )

                    redis_conn.expire(f"user:{username}", 600)
                    
                    # Create User and add
                    user = User(
                        name = name,
                        username = username,
                        email = email,
                        password = hash_password(password),
                        is_varified = False,
                        role = role
                    )

                    db.add(user)
                    db.commit()

                    # set user otp
                    key = f"{username}:otp"
                    otp = generate_otp()

                    redis_conn.set(key, otp, 600)

                    return {
                        "status" : True,
                        "message" : "OTP sent successfully.",
                        "role" : role
                    }

                else:
                    return {
                        "status" : False,
                        "message" : "Token set unsuccessfull",
                        "role" : None
                    }
                
    @classmethod
    def login(
        cls,
        username : str,
        password : str
    ):
        UserUsername = db.query(User).filter(User.username == username).first()

        # Check Username exits or not
        if UserUsername:
            if verify_password(password, UserUsername.password):
                if cls.set_session_token(username, UserUsername.role):
                    return {
                        "status" : True,
                        "message" : "login Successfull",
                        "role" : UserUsername.role
                    }
            
            else:
                return {
                    "status" : False,
                    "message" : "Incorrect Password",
                    "role" : None
                }
            
        else:
            return {
                "status" : False,
                "message" : "Username does not exits",
                "role" : None
            }

    def Logout(
        username : str
    ):
        pass
    
    @classmethod
    def have_logged_in(
        cls,
        username : str,
        token : str
    ):
        if cls.verify_session_token(username,token):
            return True
        else:
            return False
    
    @classmethod
    def set_session_token(
        cls,
        username : str,
        role : str
    ):
        cls.__username = username
        token = generate_token()

        key = cls.__username + ":" + role

        try:
            redis_conn.set(key, token, 6000)

            return True
        except:
            return False
    
    @classmethod
    def verify_session_token(
        cls,
        username : str,
        token : str
    ):
        cls.__username = username
        cls.user_token = token

        role = cls.get_user_role_by_username(cls.__username)

        if role:
            key = cls.__username + ":" + role

            redis_token = redis_conn.get(key)

            if redis_token == cls.user_token:
                return True
            
            else:
                return False
        
        else:
            return False
        

    @classmethod
    def get_user_role_by_username(
        cls,
        username : str
    ):
        stmt = (
            select(
                User.role
            )
            .where(User.username == username)
        )

        role = db.execute(stmt).first()

        if role:
            return role.role
        else:
            return None
        

    @classmethod
    def get_email_by_username(
        cls,
        username : str
    ):
        with db:
            email = db.scalar(
                select(User.email).where(User.username == username)
            )

            if email:
                return email
            else:
                return None
            
    @classmethod
    def create_and_send_otp(
        cls,
        username : str
    ):
        user_email = cls.get_email_by_username(username)

        if user_email is not None:
            otp = generate_otp()
            user_key = f"{username}:{user_email}:otp"

            redis_conn.set(user_key, otp, 600)
            redis_conn.expire(user_key, 600)

            return {
                "message" : "OTP create successfull"
            }
        else:
            return {
                'message' : "Username does not exists"
            }
        
    @classmethod
    def verify_register_otp(
        cls,
        username : str,
        user_otp : int
    ):
        key = f"{username}:otp"
        otp = redis_conn.get(key)

        if otp == user_otp:

            with db:
                user = db.scalar(
                    select(
                        User
                    ).where(User.username == username)
                )
                if user:
                    user.is_varified = True

                    db.commit()
                    redis_conn.delete(key)

                    return True
                else:
                    return {
                        "message" : "Username does not exists"
                    }
            
        else:
            return False
        
    @classmethod
    def verify_login_otp(
        cls,
        username : str,
        user_otp : int
    ):
        key = f"{username}:otp"
        otp = redis_conn.get(key)

        if otp == user_otp:
            redis_conn.delete(key)
            return True 
        else:
            return False
        