# Import standard libraries for file handling and JSON storage
import os
import json

# Import account base model and transaction logger
from models.account import Account
from models.transaction import Transaction


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

        # Structure initial account data
        new_data = {
            account_no: {}
        }

        file_path = "data/account.json"

        # Load existing data if file exists
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    data = json.load(f)
                except:
                    # Handle empty or corrupted JSON file
                    data = []
        else:
            # Initialize empty data if file does not exist
            data = []

        # Ensure data is stored as list
        if isinstance(data, dict):
            data = [data]

        # Add new account entry
        data.append(new_data)

        # Save updated data
        with open("data/account.json", "w") as f:
            json.dump(data, f, indent=4)



# =========================================================
# GET ACCOUNT DETAILS
# =========================================================
class get_account:
    """
    Retrieve and display account details for a user.
    """

    def __init__(self, username):
        self.username = username

        # Check if user file exists
        if os.path.exists("data/user.json"):
            with open("data/user.json", "r") as f:
                data = json.load(f)

                # Find matching user
                for user in data:
                    if self.username in user:

                        # Open account file
                        if os.path.exists("data/account.json"):
                            with open("data/account.json", "r") as a:
                                account_data = json.load(a)

                                # Search for user's account
                                for account in account_data:
                                    if self.username in account:
                                        print(f"Name: {account[self.username]['Name']}")
                                        print(f"Account Number: {account[self.username]['Account Number']}")
                                        print(f"Balance: {account[self.username]['Balance']}")
                                        print(f"Account Type: {account[self.username]['Account Type']}")


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

        # Ensure account file exists
        if not os.path.exists("data/account.json"):
            print("Account file not found")
            return

        # Load account data
        with open("data/account.json", "r") as f:
            data = json.load(f)

        # Search for user account
        for user in data:
            if self.account_username in user:

                Account_no = user[self.account_username]["Account Number"]
                balance = user[self.account_username]["Balance"]

                # Check sufficient balance
                if balance >= self.value:
                    balance -= self.value
                    user[self.account_username]["Balance"] = balance

                    # Save updated balance
                    with open("data/account.json", "w") as f:
                        json.dump(data, f, indent=4)

                    print("Withdraw successful")
                    print("New Balance:", balance)

                    # Record transaction log
                    Transaction(self.account_username, "Debited", self.value, balance)

                else:
                    print("Insufficient Amount")



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

        # Ensure account file exists
        if not os.path.exists("data/account.json"):
            print("Account file not found")
            return

        # Load account data
        with open("data/account.json", "r") as f:
            data = json.load(f)

        # Find user account
        for user in data:
            if self.account_username in user:
                balance = user[self.account_username]["Balance"]

                # Add deposit amount
                balance += self.value
                user[self.account_username]["Balance"] = balance

                # Save updated balance
                with open("data/account.json", "w") as f:
                    json.dump(data, f, indent=4)

                print("Deposit successful")
                print("New Balance:", balance)

                # Record transaction
                Transaction(self.account_username, "Credited", self.value, balance)



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

        # Ensure account file exists
        if not os.path.exists("data/account.json"):
            print("Account file not found")
            return

        # Load account data
        with open("data/account.json", "r") as f:
            data = json.load(f)

        # Print transaction list
        for user in data:
            if self.account_username in user:
                for trans in user[self.account_username]["Transaction"]:
                    print(trans)



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