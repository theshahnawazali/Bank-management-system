# Import required modules for file handling and JSON storage
import json
import os
from utils.auth import create_account_handle


# =========================================================
# BASE ACCOUNT CLASS
# Handles core account creation and basic balance operations
# =========================================================
class Account:
    """
    Base Account model.

    Account Number:
        type            : Account type (Saving / Current)
        name            : Account holder name
        balance         : Initial account balance
        username        : Account owner username
    """

    def __init__(self,user_id, name,account_type,account_number,balance):

        # Store account details
        self.name = name
        self.account_type = account_type
        self.user_id = user_id
        self.__account_number = int(account_number)   # Private account number
        self.__balance = int(balance)            # Private balance
        self.status = "Active"
    
        create_account_handle(self.user_id,self.__account_number,self.account_type,self.__balance,self.status)