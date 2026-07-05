# Import base Account class
from backend.app.models.account import Account
from backend.app.utils.file_handler import set_account_number
from backend.app.utils.auth import create_account_handle


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


    def __init__(self,user_id, name, account_type, account_number, balance):

        # Initialize base Account class attributes
        super().__init__(user_id, name, account_type, account_number, balance)

        # Store account details locally
        self.account_type = account_type
        self.name = name
        self.account_number = account_number