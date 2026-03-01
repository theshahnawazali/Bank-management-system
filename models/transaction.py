# =========================================================
# TRANSACTION MODULE
# Handles transaction logging (time, type, amount, balance)
# =========================================================

import os
import json
from datetime import datetime


def current_time():
    """
    Return the current system time formatted as:
    DD-MM-YYYY HH:MM:SS
    """
    now = datetime.now()
    formatted = now.strftime("%d-%m-%Y %H:%M:%S")
    return formatted


class Transaction:
    """
    Record a transaction entry for a specific account.

    Parameters:
        account_username : str  -> Account owner username
        trans_type       : str  -> Transaction type (Credited / Debited)
        amount           : int  -> Transaction amount
        total            : int  -> Updated account balance after transaction
    """

    def __init__(self, account_username, trans_type, amount, total):
        # Store transaction details
        self.account_username = account_username
        self.trans_type = trans_type
        self.amount = amount
        self.total = total

        # Automatically log transaction
        self.transacton()

    def transacton(self):
        """
        Append transaction record into account.json file.
        """

        # Ensure account file exists
        if not os.path.exists("data/account.json"):
            print("Account file not found")
            return

        # Load account data
        with open("data/account.json", "r") as f:
            data = json.load(f)

        # Search for matching user account
        for user in data:
            if self.account_username in user:

                # Append formatted transaction entry
                user[self.account_username]["Transaction"].append(
                    f"{current_time()} ---> "
                    f"{self.trans_type} | "
                    f"Amount: {self.amount} | "
                    f"Balance: {self.total}"
                )

                # Save updated transaction log
                with open("data/account.json", "w") as f:
                    json.dump(data, f, indent=4)

                break

        # If account not found, nothing happens (optional improvement: print message)