from backend.app.models.user import User
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from backend.app.models.account import Account
from backend.app.models.transaction import Transaction
from backend.app.models.requests import Request
from backend.app.utils.id_generator import generate_account_number, generate_reference_number
from datetime import datetime
from backend.app.core.config import DAILY_LIMIT
from backend.app.database.connection import redis_conn
from backend.app.services.auth_service import AuthService
from backend.app.exceptions import (
    BankAccountAlreadyExist,
    NegativeBalance,
    BankAccountNotExists,
    AccountNotActive,
    WithdrawalLimit,
    InsufficientBalance,
    TemporaryLock
)


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
        cls,
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
            raise BankAccountAlreadyExist("User have an existing account")

        UserAccount = Account(
            user_id = UserId,
            account_number = generate_account_number(),
            account_type = AccountType,
            balance = balance,
            status = status
        )

        try:
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
        
        except IntegrityError:
            db.rollback()



    @classmethod
    def get_current_user(cls, account_number : int):
        cls.__account_number = account_number
        
        user = db.query(Account).filter(Account.account_number == account_number).first()

        if user:
            return user
        
        else:
            return False

    @classmethod
    def get_balance(cls, account_number : int):
        with db:
            balance = db.scalar(
                select(Account.balance).where(Account.account_number == account_number)
            )
        
            if balance:
                username = cls.get_username_by_account_number(account_number)
                AuthService.save_audit_log(
                    username,
                    "Check Balance",
                    "123.1.1.1",
                    f"{username} balance fecth successfull",
                    AuthService.get_user_role_by_username(username),
                    "Account",
                    "Success"
                )
                return balance
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
            
    
    def get_all_accounts():
        with db:
            accounts = db.scalars(
                select(Account).join(User, User.user_id == Account.user_id)
            )

            if accounts:
                return [
                    {
                        # "username" : account.username,
                        "account number" : account.account_number,
                        "balance" : account.balance,
                        "account type" : account.account_type,
                        "status" : account.status,
                        "created at" : account.created_at
                        
                    }
                    for account in accounts
                ]
            
    @classmethod
    def freeze_account(
        cls,
        account_number : int
    ):
        with db:
            user = db.scalar(
                select(Account).where(Account.account_number == account_number)
            )

            if user:
                user.status == "Frozen"
                db.commit()
                AuthService.save_audit_log(
                    cls.get_username_by_account_number(account_number),
                    "Acoount Status",
                    "123.1.1.1",
                    "User account has been frozen",
                    "Admin",
                    "Account",
                    "Success"
                )

                return True
            else:
                AuthService.save_audit_log(
                    cls.get_username_by_account_number(account_number),
                    "Acoount Status",
                    "123.1.1.1",
                    "User account has been frozen",
                    "Admin",
                    "Account",
                    "Failed"
                )
                raise BankAccountNotExists("Account number not exists")
            
    @classmethod
    def unfreeze_account(
        cls,
        account_number : int
    ):
        with db:
            user = db.scalar(
                select(Account).where(Account.account_number == account_number)
            )

            if user:
                user.status == "Active"
                db.commit()
                AuthService.save_audit_log(
                    cls.get_username_by_account_number(account_number),
                    "Acoount Status",
                    "123.1.1.1",
                    "User account has been Active",
                    "Admin",
                    "Account",
                    "Success"
                )

                return True
            else:
                AuthService.save_audit_log(
                    cls.get_username_by_account_number(account_number),
                    "Acoount Status",
                    "123.1.1.1",
                    "User account has been Active",
                    "Admin",
                    "Account",
                    "Failed"
                )
                raise BankAccountNotExists("Account number not exists")


    @classmethod
    def deposit(
        cls,
        account_number : int,
        amount : float
    ):
        with db:
            user = db.scalar(
                select(Account).where(Account.account_number == account_number)
            )

            if user:
                user.balance += amount
                db.commit()

                AuthService.save_audit_log(
                    cls.get_username_by_account_number(account_number),
                    "Deposit",
                    "123.1.1.1",
                    f"{amount} deposited to account",
                    "Customer",
                    "Account",
                    "Success"
                )

                return user.balance
            else:
                AuthService.save_audit_log(
                    cls.get_username_by_account_number(account_number),
                    "Deposit",
                    "123.1.1.1",
                    f"{amount} deposited to account",
                    "Customer",
                    "Account",
                    "Failed"
                )
                raise BankAccountNotExists("Account number does not exists")
            
    @classmethod
    def deposit(
        cls,
        account_number : int,
        amount : float
    ):
        with db:
            user = db.scalar(
                select(Account).where(Account.account_number == account_number)
            )

            if user:
                user.balance += amount
                db.commit()

                AuthService.save_audit_log(
                    cls.get_username_by_account_number(account_number),
                    "Deposit",
                    "123.1.1.1",
                    f"{amount} deposited to account",
                    "Customer",
                    "Account",
                    "Success"
                )

                return user.balance
            else:
                AuthService.save_audit_log(
                    cls.get_username_by_account_number(account_number),
                    "Deposit",
                    "123.1.1.1",
                    f"{amount} deposited to account",
                    "Customer",
                    "Account",
                    "Failed"
                )
                raise BankAccountNotExists("Account number does not exists")
            
    @classmethod
    def withdraw(
        cls,
        account_number : int,
        amount : float
    ):
        with db:
            user = db.scalar(
                select(Account).where(Account.account_number == account_number)
            )

            if user:
                user.balance -= amount
                db.commit()

                AuthService.save_audit_log(
                    cls.get_username_by_account_number(account_number),
                    "Withdraw",
                    "123.1.1.1",
                    f"{amount} withdraw from account",
                    "Customer",
                    "Account",
                    "Success"
                )

                return user.balance
            else:
                AuthService.save_audit_log(
                    cls.get_username_by_account_number(account_number),
                    "Withdraw",
                    "123.1.1.1",
                    f"{amount} withdraw from account",
                    "Customer",
                    "Account",
                    "Failed"
                )
                raise BankAccountNotExists("Account number does not exists")
            
    @classmethod
    def transfer(
        cls,
        sender_account_number : int,
        receiver_account_number : int,
        amount : float
    ):
        with db:
            sender = db.scalar(
                select(Account).where(Account.account_number == sender_account_number)
            )

            receiver = db.scalar(
                select(Account).where(Account.account_number == receiver_account_number)
            )

            if sender:
                if receiver:
                    sender.balance -= amount
                    receiver.balance += amount

                    AuthService.save_audit_log(
                        cls.get_username_by_account_number(sender_account_number),
                        "Transfer",
                        "123.1.1.1",
                        f"{amount} transfer from to {receiver_account_number}",
                        "Customer",
                        "Account",
                        "Success"
                    )
                    return sender.balance
                else:
                    AuthService.save_audit_log(
                        cls.get_username_by_account_number(sender_account_number),
                        "Transfer",
                        "123.1.1.1",
                        f"{amount} transfer from to {receiver_account_number}",
                        "Customer",
                        "Account",
                        "Failed"
                    )
                    raise BankAccountNotExists("Receiver account does not exist")
                
            else:
                AuthService.save_audit_log(
                    cls.get_username_by_account_number(sender_account_number),
                    "Transfer",
                    "123.1.1.1",
                    f"{amount} transfer from to {receiver_account_number}",
                    "Customer",
                    "Account",
                    "Failed"
                )
                raise BankAccountNotExists("Sender account does not exist")
                                      
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
                raise AccountNotActive("Account is not active")
        else:
            raise BankAccountNotExists("Account does not exits")
        
    def get_all_transaction_history(
    ):
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
        
    @classmethod
    def get_transaction_id_history(
        cls,
        trasaction_id : str
    ):
        with db:
            historys = db.execute(
                select(
                    Transaction
                )
                .join(Account, Account.account_id == Transaction.transaction_id)
                .where(Transaction.transaction_id == trasaction_id)
            )

            if historys:
                return [
                    {
                        "account number" : history.account_number,
                        "trasaction_id" : history.transaction_id,
                        "trasaction_type" : history.transaction_type,
                        "date" : history.date,
                        "status" : history.status,
                    }
                    for history in historys
                ]
  