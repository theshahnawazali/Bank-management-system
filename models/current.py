# Import base Account class
from models.account import Account
from utils.file_handler import set_account_number


# =========================================================
# CURRENT ACCOUNT CLASS
# Represents a current account derived from base Account
# =========================================================
class Current_account(Account):
    """
    Create a Current Account instance.

    Account Number:
        {}
    """


    def __init__(self, name, type, account_no, balance, username):

        # Initialize base Account class attributes
        super().__init__(type, name, account_no, balance, username)

        # Store account details locally
        self.type = type
        self.name = name
        self.account_number = account_no
        self.username = username

        set_account_number(self.username,self.account_number)

        # Confirmation message
        print("Your Current Account is Open..")