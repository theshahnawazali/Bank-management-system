# Import base Account class
from models.account import Account
from utils.file_handler import set_account_number
from utils.auth import create_account_handle

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

    def __init__(self,user_id, name, account_type, account_number, balance):

        # Initialize base Account class attributes
        super().__init__(user_id, name, account_type, account_number, balance)

        # Store account details locally
        self.user_id = user_id
        self.name = name
        self.__balance = balance
        self.account_type = account_type
        self.account_number = account_number
        
        # set_account_number(self.username,self.account_number)
        # create_account_handle(self.user_id,self.account_number,"Saving Account",self.__balance,"Active")


