import redis
from backend.app.database.connection import SessionLocal
from backend.app.models.user import User
from backend.app.models.audit import Audit
from backend.app.database.connection import redis_conn
from backend.app.core.security import hash_password, verify_password, create_session_token
from backend.app.utils.id_generator import generate_token
from sqlalchemy import select
from backend.app.utils.id_generator import generate_otp
from backend.app.core.security import create_session_token

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
        cls.__user_email = email
        cls.__user_username = username

        # Check unique Email
        if cls.check_unique_email(cls.__user_email):
            # check unique username
            if cls.check_unique_username(cls.__user_username):
                if cls.set_session_token(username, role):
                    # check redis connection
                    redis_conn_status = True
                    if redis_conn_status:
                        pipe = redis_conn.pipeline(transaction=True)
                        pipe.hset(
                            f"user:{username}",
                            mapping={
                                "name" : name,
                                "username" : username,
                                "email" : email,
                                "password" : hash_password(password),
                                "role" : role
                            }
                        )
                        pipe.expire(f"user:{username}", 600)
                        key = f"{username}:otp"
                        otp = generate_otp()

                        pipe.set(key, otp, 600)

                        pipe.execute()

                        # save user to database
                        with db:
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

                            cls.save_audit_log(
                                cls.__user_username,
                                "Register",
                                "123.1.1.1",
                                f"{cls.__user_username} register succesfull",
                                role,
                                "User",
                                "Success"
                            )

                            return {
                                "status" : True,
                                "message" : "OTP sent successfully.",
                                "role" : role
                            }
                            
                    else:
                        cls.save_audit_log(
                            cls.__user_username,
                            "Register",
                            "123.1.1.1",
                            "Redis is not connected",
                            None,
                            "User",
                            "Failed"
                        )
                        return {
                            "status" : False,
                            "message" : "Redis is not connected",
                            "role" : None
                        }
                else:
                    cls.save_audit_log(
                        cls.__user_username,
                        "Register",
                        "123.1.1.1",
                        "Token set unsuccessfull",
                        None,
                        "User",
                        "Failed"
                    )
                    return {
                        "status" : False,
                        "message" : "Token set unsuccessfull",
                        "role" : None
                    }
            else:
                cls.save_audit_log(
                    cls.__user_username,
                    "Register",
                    "123.1.1.1",
                    f"{cls.__user_username} already exits",
                    None,
                    "User",
                    "Failed"
                )
                return {
                    "status" : username,
                    "message" : "Username already exits.",
                    "role" : None
                }
        else:
            cls.save_audit_log(
                cls.__user_username,
                "Register",
                "123.1.1.1",
                f"{cls.__user_email} already exits",
                None,
                "User",
                "Failed"
            )
            return {
                "status" : False,
                "message" : "Email already exits.",
                "role" : None
            }
                    
                
    @classmethod
    def login(
        cls,
        username : str,
        password : str
    ):

        # Check Username exits or not
        if cls.check_username_exist(username):
            if verify_password(password, cls.get_username_hashed_password(username)):
                if cls.set_session_token(username, cls.get_user_role_by_username(username)):
                    role = cls.get_user_role_by_username(username)
                    cls.save_audit_log(
                        username,
                        "Login",
                        "123.1.1.1",
                        f"{username} logged in successfull",
                        role,
                        "User",
                        "Success"
                    )
                    return {
                        "status" : True,
                        "message" : "login Successfull",
                        "role" : role
                    }
            
            else:
                cls.save_audit_log(
                    username,
                    "Login",
                    "123.1.1.1",
                    f"{username} enter incorrect password",
                    None,
                    "User",
                    "Failed"
                )
                return {
                    "status" : False,
                    "message" : "Incorrect Password",
                    "role" : None
                }
            
        else:
            cls.save_audit_log(
                username,
                "Login",
                "123.1.1.1",
                f"{username} does not exits",
                None,
                "User",
                "Failed"
            )
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
            user_key = f"{username}:otp"

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
        otp = int(redis_conn.get(key))

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
                    return False
            
        else:
            return False
        
    @classmethod
    def verify_login_otp(
        cls,
        username : str,
        user_otp : int
    ):
        key = f"{username}:otp"
        otp = int(redis_conn.get(key))

        if otp == user_otp:
            redis_conn.delete(key)
            return True 
        else:
            return False
    
    @classmethod
    def check_unique_username(
        cls,
        username : str
    ):
        with db:
            user = db.scalar(
                select(User).where(User.username == username)
            )

            if user:
                return False
            else:
                return True
    
    @classmethod
    def check_unique_email(
        cls,
        email : str
    ):
        with db:
            user = db.scalar(
                select(User).where(User.email == email)
            )

            if user:
                return False
            else:
                return True
            
    @classmethod
    def check_username_exist(
        cls,
        username : str
    ):
        with db:
            user = db.scalar(
                select(User).where(User.username == username)
            )

            if user:
                return True
            else:
                return False
            
    @classmethod
    def get_username_hashed_password(
        cls,
        username : str
    ):
        with db:
            password = db.scalar(
                select(User.password).where(User.username == username)
            )

            if password:
                return password
            else:
                return None
    @classmethod       
    def save_audit_log(
        cls,
        username : str,
        action : str,
        ip_address : str,
        description : str,
        user_role : str,
        resource : str,
        status : str
    ):
        user_id = cls.get_user_id_by_username(username)

        print(user_id)

        with db:
            log = Audit(
                user_id=user_id,
                username=username,
                action=action,
                ip_address=ip_address,
                user_role=user_role,
                description=description,
                resource=resource,
                status=status
            )

            db.add(log)
            db.commit()

    @classmethod
    def get_user_id_by_username(
        cls,
        username : str
    ):
        with db:
            userid = db.scalar(
                select(User.user_id).where(User.username == username)
            )

            if userid:
                return userid