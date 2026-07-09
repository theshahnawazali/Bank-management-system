from models.user import User
from models.account import Account
from models.requests import Request
from sqlalchemy import select
from services.bank_service import BankService
from database.connection import SessionLocal

db = SessionLocal()

class AdminService:
    @classmethod
    def check_user_exit(
        cls,
        username : str
    ):
        cls.__username = username

        stmt = (
            select(
                User.username,
                User.role
            )
            .where(User.username == cls.__username)
        )

        user = db.execute(stmt).first()

        if user:
            return True
        else:
            return False
        
    @classmethod
    def check_admin_role(
        cls,
        username : str
    ):
        cls.__username = username

        stmt = (
            select(
                User.username,
                User.role
            )
            .where(User.username == cls.__username)
        )

        user = db.execute(stmt).first()

        if user.role == "Admin":
            return True
        else:
            return False
        
    @classmethod
    def change_bank_account_status(
        cls,
        account_number  : int,
        admin_username : int,
        status : str
    ):
        cls.__admin_username = admin_username
        cls.__account_number = account_number
        account_status = ["Active", "Closed", "Frozen"]

        if status not in account_status:
            return {
                "status" : False,
                "message" : "Invalid Chnage type"
            }

        # Validate user is admin
        if cls.check_user_exit(cls.__admin_username) and cls.check_admin_role(cls.__admin_username):
            # Check account number exist
            if BankService.check_account_number_exits(cls.__account_number):
                # freeze account 

                with SessionLocal() as session:
                    user = session.scalar(
                        select(Account).where(Account.account_number == cls.__account_number)
                    )
                    
                    if user:
                        if user.status != status:
                            user.status = status
                            session.commit()

                            return {
                                "status" : True,
                                "message" : f"Account {status} successfully"
                            }

                        else:
                            return {
                                "status" : False,
                                "message" : f"Account is {user.status}"
                            }
                    else:
                        return {
                            "status" : False,
                            "message" : "Account does not exit"
                        }
                
            else:
                return {
                    "status" : False,
                    "message" : "Account number does not exit"
                }

        else:
            return {
                "status" : False,
                "message" : "User is not an admin"
            }
    
    @classmethod
    def change_user_account_status(
        cls,
        account_number : int,
        request_to : int
    ):
        cls.__account_number = account_number

        with db:
            user = db.scalar(
                select(Account).where(Account.account_number == cls.__account_number)
            )

            if user:
                if user.status == "Closed":
                    return {
                        "status" : False,
                        "message" : "Account is closed"
                    }

                elif user.status == request_to:
                    return {
                        "status" : False,
                        "message" : f"Can not set to {request_to}"
                    }
                
                else:
                    user.status = request_to

                    db.commit()

                    # with db:
                    #     request = 

                    return {
                        "status" : True,
                        "message" : "Status set successfully"
                    }
            else:
                return {
                    "status" : False,
                    "message" : "Account does not exits"
                }

       
    @classmethod
    def get_all_status_change_request(
        cls,
        admin_username : str
    ):
        if cls.check_admin_role(admin_username):
            with db:
                all_requests = db.scalars(select(Request).where(Request.request_status == "Pending")).all()

            
                return [
                    {
                        "request_id" : request.request_id,
                        "username" : None,
                        "request_from" : request.request_from,
                        "request_to" : request.request_to,
                        "status" : request.request_status,
                        "date" : request.date
                    }
                    for request in all_requests
                ]
        
        else:
            return {
                "status" : False,
                "requests" : None,
                "message" : "User is not an admin"
            }