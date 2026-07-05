import random
import secrets
from datetime import datetime
from database.connection import Session
from models.account import Account
from models.transaction import Transaction

db = Session()

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
    
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = secrets.randbelow(9000) + 1000
    reference_no = f"TXN{date_part}{random_part}"

    unique = db.query(Transaction).filter(Transaction.transaction_id == reference_no).first()

    if unique:
        return reference_no
    else:
        generate_reference_number()
    