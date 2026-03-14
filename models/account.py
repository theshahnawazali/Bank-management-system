# Import required modules for file handling and JSON storage
import json
import os


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

    def __init__(self, type, name, account_number, balance, username):

        # Store account details
        self.name = name
        self.type = type
        self.__account_number = int(account_number)   # Private account number
        self.__balance = int(balance)            # Private balance
        self.username = username

        print(self.name, self.type)

        # Structure account data for storage
        new_data = {
            self.__account_number: {
                "Name": self.name,
                "Balance": self.__balance,
                "username": self.username,
                "Account Type": self.type,
                "Transaction": []
            }
        }

        file_path = "data/account.json"

        # Load existing account data if file exists
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    data = json.load(f)
                except:
                    # Handle empty or corrupted JSON
                    data = []
        else:
            # Initialize empty data list
            data = []

        # Ensure consistent list structure
        if isinstance(data, dict):
            data = [data]

        # Append new account data
        data.append(new_data)

        # Save updated account file
        with open("data/account.json", "w") as f:
            json.dump(data, f, indent=4)
