# Import base Account class
from models.account import Account


# =========================================================
# CURRENT ACCOUNT CLASS
# Represents a current account derived from base Account
# =========================================================
class Current_account(Account):
    """
    Create a Current Account instance.

    Parameters:
        name        : Account holder name
        type        : Account type (Current Account)
        account_no  : Unique account number
        balance     : Initial account balance
        username    : Owner username
    """

    def __init__(self, name, type, account_no, balance, username):

        # Initialize base Account class attributes
        super().__init__(type, name, account_no, balance, username)

        # Store account details locally
        self.type = type
        self.name = name
        self.account_number = account_no
        self.username = username

        # Confirmation message
        print("Your Current Account is Open..")