from database.connection import Session
from models.user import User
from utils.hash import hash_password, verify_password

db = Session() # Will be removed when include fast api

class UserService:
    def Register(
            name : str,
            email : str,
            username : str,
            password : str,
            # db 
    ):
        user_username = db.query(User).filter(User.email == email).first()
        user_email = db.query(User).filter(User.username == username).first()

        # Check unique Username
        if user_username:
            return {
                "Status" : False,
                "message" : "Email already exits."
            }
        
        else:
            # Check Unique Email
            if user_email:
                return {
                    "Status" : False,
                    "message" : "Username already exits."
                }
            
            else:
                # Create User and add
                user = User(
                    username = username,
                    email = email,
                    password = hash_password(password)
                )

                db.add(user)
                db.commit()

                return {
                    "Status" : True,
                    "message" : "Account Created Successfully."
                }

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
                    "message" : "Login Successfull"
                }
            
            else:
                return {
                    "status" : False,
                    "message" : "Incorrect Password"
                }
            

        else:
            return {
                "status" : False,
                "message" : "Username does not exits"
            }

    def Logout(
            username : str
    ):
        pass