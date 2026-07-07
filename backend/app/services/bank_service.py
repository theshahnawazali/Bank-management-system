from models.user import User
from sqlalchemy import select
from models.account import Account
from models.transaction import Transaction
from receiverutils.id_generator import generate_account_number, generate_reference_number
from datetime import datetime
from core.config import DAILY_LIMIT

from database.connection import Session
db = Session()

class BankService:
    """
    Bank Service class will help us to know every details of user bank by
    just passing their account number. It has features like create account
    withdraw money, deposit money, transfer money and update transaction history,
    get user account status, get user account active status etc.
    """
    
    @staticmethod
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
    def get_balance(cls, account_number : int):
        cls.__account_number = account_number

        user = db.query(Account).filter(Account.account_number == account_number).first()
        
        return user.balance
    
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
            return {
                "status" : False,
                "Balance" : sender.balance,
                "transaction id" : None,
                "message" : "Amount can not be negative or Zero"
            }

        # Check whether sendar account exit or not
        if cls.check_user_exits(cls.__sender_account_number):
            pass
        else:
            return {
                "status" : False,
                "Balance" : None,
                "transaction id" : None,
                "message" : "Account does not exists."
            }
        
        # Check whether account is active or not
        if cls.check_account_status(cls.__sender_account_number):
            pass
        else:
            return {
                "status" : False,
                "Balance" : None,
                "transaction id" : None,
                "message" : "Account is not active"
            }

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

            return {
                "status" : True,
                "Balance" : sender.balance,
                "transaction id" : transaction_id,
                "message" : "Deposit Succesfull"
            }            

        
        #  Update withdraw balance
        elif transaction_type == "withdraw":
            # Check user have sufficient balance or not
            if sender.balance < 0 or sender.balance - cls.__amount < 0:
                cls.update_transaction(
                    cls.__sender_account_number,
                    cls.__amount,
                    "Withdraw",
                    transaction_id,
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
                    if cls.check_user_exits(cls.__receiver_account_number):

                        # Check account status
                        if cls.check_account_status(cls.__sender_account_number):

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

                            return {
                                "status" : True,
                                "Balance" : sender.balance,
                                "transaction id" : transaction_id,
                                "message" : "Withdrawal Succesfull"
                            }
                        else:
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
                            "message" : "receiver account does not exit",
                        }

                else:
                    return {
                        "status" : False,
                        "Balance" : None,
                        "transaction id" : None,
                        "message" : "Withdraw limit reached",
                    }

        #  Update transfer balance
        elif transaction_type == "transfer":

            
            # Check reciever account exit or not
            if cls.check_user_exits(cls.__receiver_account_number):

                # Check whether sender and receiver are not same
                if cls.__sender_account_number == cls.__receiver_account_number:
                    return {
                        "status" : False,
                        "Balance" : sender.balance,
                        "transaction id" : None,
                        "message" : "Can not Tranfer to same account"
                    }
                
                # Check sender and receiver are same or not
                if cls.__sender_account_number == cls.__receiver_account_number:
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

                    return {
                        "status" : True,
                        "Balance" : sender.balance,
                        "transaction id" : transaction_id,
                        "message" : "Transfer Successful",
                    }
            else:
                return {
                    "status" : False,
                    "Balance" : None,
                    "transaction id" : None,
                    "message" : "Receiver Account does not exists."
                }
            
        
        else:
            return {
                "status" : False,
                "Balance" : None,
                "transaction id" : None,
                "message" : "Invalid method"
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
        if cls.check_user_exits(cls.__account_number):
            # Check account status is active or not 
            if cls.check_account_status(cls.__account_number):
                
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

                result = db.execute(stmt).all()

                return result
            
                # return {
                #     "status" : True,
                #     "message" : "Trasaction fecth succesfull",
                #     "trasactions" : result
                # }
                
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
            return None

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
                   Transaction.date == today,
                   Transaction.status == "Success"
                )
        )    

        users = db.execute(stmt).all()

        for user in users:
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
                Account.account_number,
                Account.status
            )
            .where(Account.account_number == cls.__account_number)
        )

        user = db.execute(stmt).first()

        if user.status == "Active":
            return True
        
        else:
            return False
        

    @classmethod
    def check_user_exits(
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