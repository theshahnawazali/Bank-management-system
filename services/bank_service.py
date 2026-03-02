# Import standard libraries for file handling and JSON storage
import os
import json

# Import account base model and transaction logger
from models.account import Account
from models.transaction import Transaction

from utils import file_handler


# =========================================================
# CREATE ACCOUNT
# =========================================================
class Create_Account:
    """
    Create a new account entry in account.json.
    Initializes account storage for a user.
    """

    def __init__(self, account_no):
        self.account_no = account_no

        file_handler.create_account_handle(account_no)


# =========================================================
# GET ACCOUNT DETAILS
# =========================================================
class get_account:
    """
    Retrieve and display account details for a user.
    """

    def __init__(self, username):
        self.username = username

        file_handler.get_account_handle(self.username)    


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
        
        file_handler.withdraw_handle(self.account_username,self.value)
        



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
        file_handler.deposit_handle(self.account_username,self.value)


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
        file_handler.transaction_handler(self.account_username)
        



# =========================================================
# DELETE ACCOUNT (Not implemented yet)
# =========================================================
class Delete(Account):
    """
    Placeholder for account deletion logic.
    """
    pass


# =========================================================
# FUTURE FEATURES
# =========================================================