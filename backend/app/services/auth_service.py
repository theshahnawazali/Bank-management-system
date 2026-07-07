from database.connection import Session
from models.user import User
from utils.security import hash_password, verify_password

db = Session() # Will be removed when include fast api

class UserService:
    @staticmethod
    def Register(
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
                # Create User and add
                user = User(
                    name = name,
                    username = username,
                    email = email,
                    password = hash_password(password),
                    role = role
                )

                db.add(user)
                db.commit()

                return {
                    "status" : True,
                    "message" : "Account Created Successfully.",
                    "role" : role
                }
            
    @staticmethod
    def Login(
            username : str,
            password : str
    ):
        UserUsername = db.query(User).filter(User.username == username).first()

        # Check Username exits or not
        if UserUsername:
            if verify_password(password, UserUsername.password):
                return {
                    "status" : True,
                    "message" : "Login Successfull",
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

    def have_logged_in(
            username : str
    ):
        pass