import random
from data.db import cursor
import secrets
from datetime import datetime

# Generate a unique account number and verify it is unique

def generate_acc():
    account_number = random.randint(100000000000, 999999999999)
    cursor.execute(f"""
        SELECT account_number FROM accounts WHERE account_number = {account_number}
    """)
    unique = cursor.fetchone()

    if unique == None:
        return account_number
    else:
        generate_acc()
    


    

# Ensure the username is unique
def check_username(username):
    cursor.execute(f"""
        SELECT username FROM users WHERE username = '{username}'
    """)

    unique = cursor.fetchone()
    if unique == None:
        return True
    else:
        return False
    
# Generates Reference number and ensure it is unique
def generate_reference_number():
    
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = secrets.randbelow(9000) + 1000
    reference_no = f"TXN{date_part}{random_part}"

    return reference_no
    