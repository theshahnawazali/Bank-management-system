# Import account base model and transaction logger
from models.account import Account
from utils import file_handler
from models.transaction import Transaction

# =========================================================
# CREATE ACCOUNT
# =========================================================
class Create_Account:
    """
    Create a new account entry in account.json.
    Initializes account storage for a user.
    """

    def __init__(self, account_number):
        self.account_no = account_number

        file_handler.create_account_handle(account_number)


# =========================================================
# GET ACCOUNT DETAILS
# =========================================================
class get_account:
    """
    Retrieve and display account details for a user.
    """

    def __init__(self, username):
        self.username = username

        self.info = file_handler.get_account_handle(self.username)


# =========================================================
# WITHDRAW MONEY
# =========================================================
class Withdraw:
    """
    Withdraw amount from user's account if sufficient balance exists.
    """

    def __init__(self, account_username, value):
        self.account_username = account_username
        self.value = value
        self.withdraw()

    def withdraw(self):
        
        self.withdraw = file_handler.withdraw_handle(self.account_username,self.value)

        Transaction(
            self.account_username,
            "Withdraw",
            self.value
        )
        



# =========================================================
# DEPOSIT MONEY
# =========================================================
class Deposit:
    """
    Deposit amount into user's account.
    """

    def __init__(self, account_username, value):
        self.account_username = account_username
        self.value = value
        self.deposit()

    def deposit(self):
        self.deposit = file_handler.deposit_handle(self.account_username,self.value)

        Transaction(
            self.account_username,
            "Deposits",
            self.value
        )


# =========================================================
# SHOW TRANSACTION HISTORY
# =========================================================
class Transactions:
    """
    Display transaction history for a user.
    """

    def __init__(self, username):
        self.account_username = username
        self.transaction()

    def transaction(self):
        self.trans = file_handler.transaction_handler(self.account_username)
        
        



# =========================================================
# DELETE ACCOUNT (Not implemented yet)
# =========================================================
class Delete(Account):
    """
    Placeholder for account deletion logic.
    """
    pass

# =========================================================
# TRANSFER MONEY
# =========================================================
class Transfer:
    def __init__(self,username,value,account_number):
        self.username =username
        self.value = value
        self.account_number = account_number
        self.transfer()

    def transfer(self):
            self.transfer = file_handler.transfer_handle(self.username,self.value,self.account_number)

            Transaction(
                self.username,
                "Transfer",
                self.value,
            )
            
            


# =========================================================
# FUTURE FEATURES
# =========================================================