from backend.app.models.user import User
from sqlalchemy import select
from backend.app.models.account import Account
from backend.app.models.transaction import Transaction
from backend.app.models.requests import Request
from backend.app.utils.id_generator import generate_account_number, generate_reference_number
from datetime import datetime
from backend.app.core.config import DAILY_LIMIT
from backend.app.database.connection import redis_conn
from backend.app.services.auth_service import AuthService

from backend.app.database.connection import SessionLocal
db = SessionLocal()

class BankService:
    """
    Bank Service class will help us to know every details of user bank by
    just passing their account number. It has features like create account
    withdraw money, deposit money, transfer money and update transaction history,
    get user account status, get user account active status etc.
    """
    
    @classmethod
    def create_account(
            username : str,
            AccountType : str,
            balance : float,
            status : str
    ):
        UserUsername = db.query(User).filter(User.username == username).first()
        UserId = UserUsername.user_id

        id = db.query(Account).filter(Account.user_id == UserId).first()

        if id:
            AuthService.save_audit_log(
                username,
                "Create Account",
                "123.1.1.1",
                f"{username} have an exiting account",
                AuthService.get_user_role_by_username(username),
                "Account",
                "Failed"
            )
            return {
                "status" : False,
                "message" : "User have an exiting account"
            }

        UserAccount = Account(
            user_id = UserId,
            account_number = generate_account_number(),
            account_type = AccountType,
            balance = balance,
            status = status
        )

        db.add(UserAccount)
        db.commit()

        AuthService.save_audit_log(
            username,
            "Create Account",
            "123.1.1.1",
            f"{username} account created successfully",
            AuthService.get_user_role_by_username(username),
            "Account",
            "Success"
        )
        return {
            "status" : True,
            "message" : "Account created successfully"
        }

    @classmethod
    def get_current_user(cls, account_number : int):
        cls.__account_number = account_number
        
        user = db.query(Account).filter(Account.account_number == account_number).first()

        if user:
            return user
        
        else:
            return False

    @classmethod
    def get_balance(cls, account_id : int):
        
        if cls.get_account_number_by_id(account_id):
            cls.__account_number = cls.get_account_number_by_id(account_id)
            user = db.query(Account).filter(Account.account_number == cls.__account_number).first()

            username = cls.get_username_by_account_number(cls.__account_number)
            AuthService.save_audit_log(
                username,
                "Check Balance",
                "123.1.1.1",
                f"{username} balance fecth successfull",
                AuthService.get_user_role_by_username(username),
                "Account",
                "Success"
            )
        
            return user.balance
        else:
            AuthService.save_audit_log(
                None,
                "Check Balance",
                "123.1.1.1",
                f"balance fecth unsuccessfull",
                None,
                "Account",
                "Failed"
            )
            return False
        
        
    
    @classmethod
    def UpdateBalance(
        cls,
        sendar_account_number : int,
        amount : int,
        transaction_type : str,
        receiver_account_number : int = None,
    ):
        cls.__sender_account_number = sendar_account_number
        cls.__receiver_account_number = receiver_account_number
        cls.__amount = amount
        sender = cls.get_current_user(cls.__sender_account_number)
        receiver = cls.get_current_user(cls.__receiver_account_number)
        transaction_id = generate_reference_number()

        # Check user login

        # Check Amount > 0
        if cls.__amount <= 0:
            AuthService.save_audit_log(
                cls.get_username_by_account_number(cls.__sender_account_number),
                "Update Balance",
                "123.1.1.1",
                "Amount can not be negative or Zero",
                None,
                "Account",
                "Failed"
            )
            return {
                "status" : False,
                "Balance" : sender.balance,
                "transaction id" : None,
                "message" : "Amount can not be negative or Zero"
            }

        # Check whether sendar account exit or not
        if cls.check_account_number_exits(cls.__sender_account_number):
            lock = redis_conn.lock(cls.__sender_account_number, timeout=30)

        else:
            AuthService.save_audit_log(
                cls.get_username_by_account_number(cls.__sender_account_number),
                "Update Balance",
                "123.1.1.1",
                "Account does not exists.",
                None,
                "Account",
                "Failed"
            )
            return {
                "status" : False,
                "Balance" : None,
                "transaction id" : None,
                "message" : "Account does not exists."
            }
        
        # Check whether account is active or not
        if not cls.check_account_status(cls.__sender_account_number) == "Active":
            AuthService.save_audit_log(
                cls.get_username_by_account_number(cls.__sender_account_number),
                "Update Balance",
                "123.1.1.1",
                "Account is not active",
                None,
                "Account",
                "Failed"
            )
            return {
                "status" : False,
                "Balance" : None,
                "transaction id" : None,
                "message" : "Account is not active"
            }
        
        if lock.acquire():
            try:                
                #  Update deposit balance
                if transaction_type == "deposit":
                            
                    # Update Balance
                    sender.balance += cls.__amount
                    db.commit()

                    # Update Transaction history
                    cls.update_transaction(
                        cls.__sender_account_number,
                        cls.__amount,
                        "Deposit",
                        transaction_id,
                        "Success"
                    )

                    AuthService.save_audit_log(
                        cls.get_username_by_account_number(cls.__sender_account_number),
                        "Deposit",
                        "123.1.1.1",
                        "Deposit Succesfull",
                        None,
                        "Account",
                        "Success"
                    )
                    return {
                        "status" : True,
                        "Balance" : sender.balance,
                        "transaction id" : transaction_id,
                        "message" : "Deposit Succesfull"
                    }            

                
                #  Update withdraw balance
                elif transaction_type == "withdraw":
                    # Check user have sufficient balance or not
                    if sender.balance - cls.__amount < 0:
                        cls.update_transaction(
                            cls.__sender_account_number,
                            cls.__amount,
                            "Withdraw",
                            transaction_id,
                            "Failed"
                        )

                        AuthService.save_audit_log(
                            cls.get_username_by_account_number(cls.__sender_account_number),
                            "Deposit",
                            "123.1.1.1",
                            f"{cls.get_username_by_account_number(cls.__sender_account_number)} have insufficient Amount",
                            None,
                            "Account",
                            "Failed"
                        )

                        return {
                            "status" : False,
                            "Balance" : sender.balance,
                            "transaction id" : None,
                            "message" : "Insufficient Amount",
                        }
                    else:
                        # Check user widrawal limit for today
                        if cls.get_user_withdrawal_limit(cls.__sender_account_number):

                            # Check Reciever account exist
                            if cls.check_account_number_exits(cls.__sender_account_number):

                                # Check account status
                                if cls.check_account_status(cls.__sender_account_number) == "Active":

                                    # Update Balance
                                    sender.balance -= cls.__amount
                                    db.commit()

                                    # Update Transaction
                                    cls.update_transaction(
                                        cls.__sender_account_number,
                                        cls.__amount,
                                        "Withdraw",
                                        transaction_id,
                                        "Success"
                                    )

                                    AuthService.save_audit_log(
                                        cls.get_username_by_account_number(cls.__sender_account_number),
                                        "Deposit",
                                        "123.1.1.1",
                                        f"{cls.get_username_by_account_number(cls.__sender_account_number)} withdrawal successfull",
                                        None,
                                        "Account",
                                        "Success"
                                    )

                                    return {
                                        "status" : True,
                                        "Balance" : sender.balance,
                                        "transaction id" : transaction_id,
                                        "message" : "Withdrawal Succesfull"
                                    }
                                else:
                                    AuthService.save_audit_log(
                                        cls.get_username_by_account_number(cls.__sender_account_number),
                                        "Deposit",
                                        "123.1.1.1",
                                        f"{cls.get_username_by_account_number(cls.__sender_account_number)} account is not active",
                                        None,
                                        "Account",
                                        "Failed"
                                    )
                                    return {
                                        "status" : False,
                                        "Balance" : None,
                                        "transaction id" : None,
                                        "message" : "Account is not active",
                                    }
                            else:
                                return {
                                    "status" : False,
                                    "Balance" : None,
                                    "transaction id" : None,
                                    "message" : "Sender account does not exit",
                                }

                        else:
                            AuthService.save_audit_log(
                                cls.get_username_by_account_number(cls.__sender_account_number),
                                "Deposit",
                                "123.1.1.1",
                                f"{cls.get_username_by_account_number(cls.__sender_account_number)} withdraw limit reached",
                                None,
                                "Account",
                                "Failed"
                            )
                            return {
                                "status" : False,
                                "Balance" : None,
                                "transaction id" : None,
                                "message" : "Withdraw limit reached",
                            }

                #  Update transfer balance
                elif transaction_type == "transfer":

                    
                    # Check reciever account exit or not
                    if cls.check_account_number_exits(cls.__receiver_account_number):

                        # Check whether sender and receiver are not same
                        if cls.__sender_account_number == cls.__receiver_account_number:
                            AuthService.save_audit_log(
                                cls.get_username_by_account_number(cls.__sender_account_number),
                                "Transfer",
                                "123.1.1.1",
                                f"{cls.get_username_by_account_number(cls.__sender_account_number)} can not Tranfer to same account",
                                None,
                                "Account",
                                "Failed"
                            )
                            return {
                                "status" : False,
                                "Balance" : sender.balance,
                                "transaction id" : None,
                                "message" : "Can not Tranfer to same account"
                            }

                        # Check where sender have enough balance
                        if sender.balance < 0 or sender.balance - cls.__amount < 0:
                            cls.update_transaction(
                                cls.__sender_account_number,
                                cls.__amount,
                                "Transfer",
                                transaction_id,
                                "Failed"
                            )
                            AuthService.save_audit_log(
                                cls.get_username_by_account_number(cls.__sender_account_number),
                                "Transfer",
                                "123.1.1.1",
                                f"{cls.get_username_by_account_number(cls.__sender_account_number)} have in sufficient amount",
                                None,
                                "Account",
                                "Failed"
                            )
                            return {
                                "status" : False,
                                "Balance" : sender.balance,
                                "transaction id" : None,
                                "message" : "Insufficient Amount",
                            }
                        else:
                            sender.balance -= cls.__amount
                            receiver.balance += cls.__amount

                            cls.update_transaction(
                                cls.__sender_account_number,
                                cls.__amount,
                                "Transfer",
                                transaction_id,
                                "Success"
                            )

                            db.commit()

                            cls.update_transaction(
                                cls.__receiver_account_number,
                                cls.__amount,
                                "Recieve",
                                transaction_id,
                                "Success"
                            )
                            
                            AuthService.save_audit_log(
                                cls.get_username_by_account_number(cls.__sender_account_number),
                                "Transfer",
                                "123.1.1.1",
                                f"{cls.get_username_by_account_number(cls.__sender_account_number)} trasfered amount to {cls.get_username_by_account_number(cls.__receiver_account_number)}",
                                None,
                                "Account",
                                "Success"
                            )

                            return {
                                "status" : True,
                                "Balance" : sender.balance,
                                "transaction id" : transaction_id,
                                "message" : "Transfer Successful",
                            }
                    else:
                        AuthService.save_audit_log(
                                cls.get_username_by_account_number(cls.__sender_account_number),
                                "Transfer",
                                "123.1.1.1",
                                "Reciever account does not exits",
                                None,
                                "Account",
                                "Failed"
                            )
                        return {
                            "status" : False,
                            "Balance" : None,
                            "transaction id" : None,
                            "message" : "Receiver Account does not exists."
                        }
                    
                
                else:
                    AuthService.save_audit_log(
                        cls.get_username_by_account_number(cls.__sender_account_number),
                        "Update Balance",
                        "123.1.1.1",
                        "Invalid method",
                        None,
                        "Account",
                        "Failed"
                    )
                    return {
                        "status" : False,
                        "Balance" : None,
                        "transaction id" : None,
                        "message" : "Invalid method"
                    }
                
            finally:
                lock.release()

        else:
            AuthService.save_audit_log(
                cls.get_username_by_account_number(cls.__sender_account_number),
                "Update Balance",
                "123.1.1.1",
                "Account is temporiry lock",
                None,
                "Account",
                "Failed"
            )
            return {
                "status" : False,
                "Balance" : None,
                "transaction id" : None,
                "message" : "Account is temporiry lock"
            }

    @classmethod
    def update_transaction(
            cls,
            account_number : int,
            amount : float,
            transaction_type : str,
            transaction_id : str,
            status : str
        ):
        cls.__account_number = account_number
        cls.__amount = amount

        try:
            CurrentUser = db.query(Account).filter(Account.account_number == cls.__account_number).first()


            Current_transaction = Transaction(
                account_id = CurrentUser.account_id,
                amount = cls.__amount,
                transaction_id = transaction_id,
                transaction_type = transaction_type,
                status = status
            )

            db.add(Current_transaction)
            db.commit()

            return True
        
        except:
            return False
        

    @classmethod
    def get_transaction_history(
        cls,
        account_number : int
    ):
        cls.__account_number = account_number
        # Check account exists
        if cls.check_account_number_exits(cls.__account_number):
            # Check account status is active or not 
            if cls.check_account_status(cls.__account_number) == 'Active':
                
                stmt = (
                    select(
                        Account.account_id,
                        Account.account_number,
                        Transaction.transaction_id,
                        Transaction.transaction_type,
                        Transaction.amount,
                        Transaction.date,
                        Transaction.status,
                    )
                    .join(Account, Account.account_id == Transaction.account_id)
                    .where(Account.account_number == cls.__account_number)
                )

                rows = db.execute(stmt).all()

                return [
                    {
                        "account_id": row.account_id,
                        "account_number": row.account_number,
                        "transaction_id": row.transaction_id,
                        "transaction_type": row.transaction_type,
                        "amount": row.amount,
                        "date": row.date,
                        "status": row.status,
                    }
                    for row in rows
                ]
            
            else:
                return {
                    "status" : False,
                    "message" : "Account is not active",
                    "trasactions" : None
                }

        else:
            return {
                "status" : False,
                "message" : "Account does not exist",
                "trasactions" : None
            }
        
    @classmethod
    def get_account_details(
        cls,
        account_number: int
    ):
        """
        This fuction help us to find user name, username, email, balance,
        status, account created time, account tye by just giving users account number.
        """

        cls.__account_number = account_number
        stmt = (
            select(
                User.name,
                User.username,
                User.email,
                Account.account_id,
                Account.balance,
                Account.status,
                Account.created_at,
                Account.account_type
            )
            .join(Account, User.user_id == Account.user_id)
            .where(Account.account_number == cls.__account_number)
        )

        result = db.execute(stmt).first()

        if result is None:
            AuthService.save_audit_log(
                cls.get_username_by_account_number(cls.__account_number),
                "Account Detail",
                "123.1.1.1",
                "Account not found",
                None,
                "Account",
                "Failed"
            )
            return None

        else:
            AuthService.save_audit_log(
                cls.get_username_by_account_number(cls.__account_number),
                "Account Detail",
                "123.1.1.1",
                "Account request fetch successful",
                None,
                "Account",
                "Success"
            )

            return result
    
    @classmethod
    def get_user_withdrawal_limit(
        cls,
        account_number : int
    ):
        """
            This function help us to check whether account withdrawal balance have reaced DAILY limit or no.
        """

        today = datetime.now().strftime("%d/%m/%Y")
        Amount = 0

        stmt = (
            select(
                Account.account_number,
                Transaction.amount,
                Transaction.transaction_type,
                Transaction.date,
                Transaction.status
            )
            .join(Transaction, Transaction.account_id == Account.account_id)
            .where(Account.account_number == account_number,
                   Transaction.transaction_type == "withdraw",
                   Transaction.status == "Success"
                )
        )    

        users = db.execute(stmt).all()

        for user in users:
            if today == user.date.strftime("%d/%m/%Y"):
                Amount += user.amount
    
        if Amount < DAILY_LIMIT:
            return True
        else:
            return False
        
    @classmethod
    def check_account_status(
        cls,
        account_number : int
    ):
        cls.__account_number = account_number

        stmt = (
            select(
                Account.status
            )
            .where(Account.account_number == cls.__account_number)
        )

        user = db.execute(stmt).first()

        return user.status
        

    @classmethod
    def check_account_number_exits(
        cls,
        account_number : int
    ):
        cls.__account_number = account_number

        stmt = (
            select(
                Account.account_number
            )
            .where(Account.account_number == cls.__account_number)
        )

        user = db.execute(stmt).first()

        if user:
            return True
        else:
            return False
        
    @classmethod
    def check_username_exits(
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
    def get_account_number_by_id(
        cls,
        account_id : int
    ):
        stmt = (
            select(
                Account.account_id,
                Account.account_number
            )
            .where(Account.account_id == account_id)
        )

        account_number = db.execute(stmt).first()

        if account_number:
            return account_number.account_number
        
    @classmethod    
    def request_to_change_account_status(
        cls,
        account_number : int,
        request_to : str
    ):
        cls.__account_number = account_number

        user = cls.get_account_details(cls.__account_number)

        if user.status == request_to or user.status == "Closed":
            AuthService.save_audit_log(
                cls.get_username_by_account_number(cls.__account_number),
                "Request",
                "123.1.1.1",
                f"Request cancel due to user is already {request_to}",
                "Customer",
                "Account",
                "Failed"
            )
            return {
                "status" : False,
                "message" : f"Account is  {request_to}"
            }
        else:
            with db:
                change_request = Request(
                    account_id = user.account_id,
                    request_from = user.status,
                    request_to = request_to,
                    request_status = "Pending"
                )

                db.add(change_request)
                db.commit()
            
            AuthService.save_audit_log(
                cls.get_username_by_account_number(cls.__account_number),
                "Request",
                "123.1.1.1",
                "Status change request accepted",
                "Customer",
                "Account",
                "Success"
            )
            return {
                "status" : True,
                "message" : "Change request sent successfull"
            }
     
# To be build  
    @classmethod
    def delete_user(
        cls,
        user_username : int,
    ):
        cls.__user_username = user_username
        cls.__account_number = cls.get_account_number_by_username(cls.__user_username)
        print(cls.__account_number)
        if cls.check_account_number_exits(cls.__account_number):
            if cls.check_account_status(cls.__account_number) == "Closed":
                with db:
                    user = db.scalar(
                        select(User).where(User.username == cls.__user_username)
                    )
                                    
                    if user:
                        # db.delete(user)
                        # db.commit()

                        return {
                            "status" : True,
                            "message" : "User delete successfull"
                        }
                    
                    else:
                        return {
                            "status" : False,
                            "message" : "User does not exit"
                        }
            else:
                return {
                    "status" : False,
                    "message" : "Account is not active"
                }
        else:
            return {
                "status" : False,
                "message" : "Account number does not exit"
            }

    @classmethod
    def get_account_number_by_username(
        cls,
        username : str
    ):
        with db:
            account_number = db.scalar(
                select(
                    Account.account_number
                )
                .join(User, Account.user_id == User.user_id)
                .where(User.username == username)
            )

            return account_number
        
    @classmethod
    def get_username_by_account_number(
        cls,
        account_number : int
    ):
        with db:
            user = db.scalar(
                select(
                    User.username
                )
                .join(Account, Account.user_id == User.user_id)
                .where(Account.account_number == account_number)
            )

            if user:
                return user
            else:
                return None