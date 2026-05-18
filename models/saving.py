# Import base Account class
from models.account import Account
from utils.file_handler import set_account_number

# =========================================================
# SAVING ACCOUNT CLASS
# Represents a saving account type derived from base Account
# =========================================================
class saving_account(Account):
    """
    Create a Saving Account instance.

    Account Number:
        {}
    """

    def __init__(self, name, type, account_number, balance, username):

        # Initialize base Account class attributes
        super().__init__(type, name, account_number, balance, username)

        # Store account details locally
        self.__balance = balance
        self.type = type
        self.name = name
        self.account_number = account_number
        self.username = username
        
        set_account_number(self.username,self.account_number)
