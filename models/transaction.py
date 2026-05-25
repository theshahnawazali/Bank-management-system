# =========================================================
# TRANSACTION MODULE
# Handles transaction logging (time, type, amount, balance)
# =========================================================

import os
import json
from datetime import datetime
from utils.file_handler import update_transaction, get_username_via_account_number


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
        type             : str  -> Transaction Stutus
    """

    def __init__(
            self,
            account_username : str,
            trans_type       : str,
            amount           : int,
            account_number   : int = None,
            status           : str = "Success"
    ):
        # Store transaction details
        self.account_username = account_username
        self.trans_type = trans_type
        self.account_number = account_number
        self.amount = amount
        self.status = status

        # Automatically log transaction
        self.transacton()

    def transacton(self):
        """
        Append transaction record into account.json file.
        """

        update_transaction(
            self.account_username,
            self.amount,
            self.trans_type,
            self.status
        )

        if self.trans_type == "Transfer":
            self.update_reciever_transaction()

    def update_reciever_transaction(self):
        reciever_username = get_username_via_account_number(self.account_number)

        update_transaction(
            reciever_username,
            self.amount,
            "Recieved",
            self.status
        )