# Import base Account class
from models.account import Account


# =========================================================
# SAVING ACCOUNT CLASS
# Represents a saving account type derived from base Account
# =========================================================
class saving_account(Account):
    """
    Create a Saving Account instance.

    Parameters:
        name        : Account holder name
        type        : Account type (Saving Account)
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
        print("Your Saving Account is Open..")