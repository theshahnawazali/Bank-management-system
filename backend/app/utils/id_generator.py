import random
import secrets
import uuid
from datetime import datetime
from backend.app.database.connection import SessionLocal
from backend.app.models.account import Account
from backend.app.models.transaction import Transaction
import secrets

db = SessionLocal()

# Generate a unique account number and verify it is unique

def generate_account_number():
    account_number = random.randint(100000000000, 999999999999)

    unique = db.query(Account).filter(Account.account_number == account_number).first()

    if unique == None:
        return account_number
    else:
        generate_account_number()


# Generates Reference number and ensure it is unique
def generate_reference_number():
    transaction_id = "TXN" + uuid.uuid4().hex[:16].upper()

    unique = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()

    if unique == None:
        return transaction_id
    else:
        generate_reference_number()
    
def generate_token():
    return secrets.token_hex(10)

