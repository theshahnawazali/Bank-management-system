from models.user import User
from models.account import Account
from utils.generator import generate_account_number, generate_reference_number

from database.connection import Session
db = Session()

class BankService:
    def create_account(
            username : str,
            AccountType : str,
            balance : float,
            status : str
    ):
        UserUsername = db.query(User).filter(User.username == username).first()
        UserId = UserUsername.user_id

        UserAccount = Account(
            user_id = UserId,
            account_number = generate_account_number(),
            balance = balance,
            account_type = AccountType,
            status = status
        )

        db.add(UserAccount)
        db.commit()

        return {
            "status" : True,
            "message" : "Account created successfully"
        }


    def get_current_user(self, account_number : int):
        self.__account_number = account_number
        
        user = db.query(Account).filter(Account.account_number == account_number).first()

        if user:
            return user
        
        else:
            return False

    def get_balance(account_number : int):
        account_number = account_number

        user = db.query(Account).filter(Account.account_number == account_number).first()
        
        return user.balance

    def deposit(self, account_number : int, amount : float):
        self.__account_number = account_number
        self.__amount = amount
        
        balance = self.get_balance(self.__account_number)

        user = self.get_current_user(account_number)

        user.balance += balance

        return user.balance
        

    def withdraw(self, account_number : int, amount : float):
        self.__account_number = account_number
        self.__amount = amount

        balance = self.get_balance(self.__account_number)
        
        user = self.get_current_user(account_number)
        user.balance -= balance

        return user.balance

    def transfer(self, account_number : int):
        self.account_number = account_number
        pass

    def get_transaction_history(self, account_number : int):
        self.__account_number = account_number
        
        user = self.get_current_user(account_number)

        
    def get_username_by_account_number(self, account_number):
        self.__account_number = account_number
        
        user = db.query(Account, User).join(User).filter(Account.account_number == self.__account_number).first()

        # Have not competed yet

    def update_transaction(
            self,
            account_number : int,
            amount : float,
            transaction_type : str,
            status : str
        ):
        self.__account_number = account_number
        self.__amount = amount

        try:
            CurrentUser = db.query(Account).filter(Account.account_number == self.__account_number).first()
            
            Current_transaction = Account(
                account_id = CurrentUser.account_id,
                amount = self.__amount,
                transaction_id = generate_reference_number(),
                transaction_type = transaction_type,
                status = status
            )

            db.add(Current_transaction)
            db.commit()

            return True
        
        except:
            return False