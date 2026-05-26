# =========================================================
# FILE HANDLING
# Centralized File Handling logic for banking system
# =========================================================

import os
import json
from utils.generator import generate_reference_number
from data.db import cursor, conn

# --------------- Signup Handler ----------------
def signup_handle(username,name,password):
    # Structure new user data
        new_data = {
            username: {
                "Name": name,
                "Password": password
            }
        }

        file_path = "data/user.json"

        # Load existing user data if file exists
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    data = json.load(f)
                except:
                    # Handle empty or corrupted JSON file
                    data = []
        else:
            # Initialize empty list if file does not exist
            data = []

        # Ensure data format is always a list
        if isinstance(data, dict):
            data = [data]

        # Append new user record
        data.append(new_data)

        # Save updated user data back to file
        with open("data/user.json", "w") as f:
            json.dump(data, f, indent=4)


# --------------- Login Handler ----------------
def login_handle(username,password):
    file_path = "data/user.json"
    found = False  # Track if user exists

    # Check if user data file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                data = json.load(f)

                # Iterate through stored users
                for user in data:
                    if username in user:
                        found = True

                        # Validate password
                        if user[username]["Password"] == password:
                            return True
                        else:
                            return False

                # If username not found in file
                if not found:
                    return "user not found"

            except json.JSONDecodeError:
                # Handle invalid JSON format
                print("Invalid Json Format")


# --------------- Create Account Handler ----------------
def create_account_handle(account_number):
    # Structure initial account data
    new_data = {
        account_number: {}
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


# --------------- Get Account Handler ----------------
def get_account_handle(username):
        cursor.execute(f"""
            SELECT users.full_name, users.user_id FROM users JOIN accounts ON users.user_id = accounts.user_id WHERE username = '{username}';
        """)
        user_data = cursor.fetchone()

        cursor.execute(f"""
            SELECT account_number, account_type, balance, status, created_at FROM accounts WHERE user_id = {user_data[1]}
        """)
        account_data = cursor.fetchone()

        info = {
            "Name"              : user_data[0],
            "Balance"           : account_data[2],
            "Account Type"      : account_data[1],
            "Account Number "   : account_data[0],
            "Account Username"  : username,
            "Account Status"    : account_data[3],
            "Open On"           : account_data[4]
        }
        return info

# --------------- Withdraw Handler ----------------
def withdraw_handle(username,value):
    cursor.execute(f"""
        SELECT users.full_name, users.user_id FROM users JOIN accounts ON users.user_id = accounts.user_id WHERE username = '{username}';
    """)
    user_data = cursor.fetchone()

    cursor.execute(f"""
        SELECT balance FROM accounts WHERE user_id = {user_data[1]}
                   """)
    
    amount = cursor.fetchone()

    if value <= amount[0]:
        cursor.execute("""
            UPDATE accounts SET balance = balance - %s WHERE user_id = %s   
        """,(value,user_data[1]))

        conn.commit()
        return True
    
    return False

# --------------- Deposit Handler ----------------
def deposit_handle(username,value):
    cursor.execute(f"""
        SELECT users.full_name, users.user_id FROM users JOIN accounts ON users.user_id = accounts.user_id WHERE username = '{username}';
    """)
    user_data = cursor.fetchone()

    cursor.execute(f"""
        SELECT balance FROM accounts WHERE user_id = {user_data[1]}
                   """)
    
    amount = cursor.fetchone()

    if amount[0] > 0:
        cursor.execute("""
            UPDATE accounts SET balance = balance + %s WHERE user_id = %s   
        """,(value,user_data[1]))

        conn.commit()
        return True
    
    return False

                # Record transaction
                # Transaction(acc_no, "Credited", value, balance)


# --------------- Transaction Handler ----------------
def transaction_handler(username):
    cursor.execute(f"""
        SELECT 
            transactions.transaction_id, 
            transactions.transaction_type, 
            transactions.transaction_date,
            transactions.amount,
            transactions.transaction_status
        FROM users
        JOIN accounts 
            ON users.user_id = accounts.user_id
        JOIN transactions 
            ON transactions.account_id = accounts.account_id
        WHERE username = '{username}';
    """)

    data = cursor.fetchall()
    
    return data

def update_transaction(username,amount,transaction_type,transaction_status):
    cursor.execute("""
        SELECT user_id FROM users WHERE username = %s
                   """,(username,))
    
    user_id = cursor.fetchone()

    cursor.execute("""
        SELECT account_id FROM accounts WHERE user_id = %s
                   """,(user_id[0],))
    
    account = cursor.fetchone()

    transaction_id = generate_reference_number()

    cursor.execute("""
        INSERT INTO transactions (account_id,amount, transaction_id, transaction_type, transaction_status) VALUE (%s, %s, %s, %s, %s)
    """,(account[0],amount,transaction_id,transaction_type,transaction_status))

    conn.commit()


def get_username_via_account_number(account_number):
    cursor.execute("""
        SELECT users.username, accounts.account_number   FROM users JOIN accounts ON users.user_id = accounts.user_id WHERE account_number = %s;
                   """,(account_number,))
    
    reciever_username = cursor.fetchone()

    return reciever_username[0]

# --------------- Set Account Number ----------------
def set_account_number(username,account_number):
    if not os.path.exists("data/user.json"):
        print("User Path not found.")
        return
    
    with open("data/user.json","r") as f:
        try:
            data = json.load(f)
        except:
            data = []

    for users in data:
        if username in users:
            users[username]["Account Number"] =  account_number

    with open("data/user.json", "w") as f:
            json.dump(data, f, indent=4)

# --------------- Transfer Handler ----------------
def transfer_handle(username,value,account_number):
    cursor.execute(f"""
        SELECT users.full_name, users.user_id FROM users JOIN accounts ON users.user_id = accounts.user_id WHERE username = '{username}';
    """)
    user_id = cursor.fetchone()

    cursor.execute(f"""
        SELECT balance FROM accounts WHERE user_id = {user_id[1]}
                   """)
    
    amount = cursor.fetchone()

    if value <= amount[0]:
        cursor.execute("""
            UPDATE accounts SET balance = balance - %s WHERE user_id = %s   
        """,(value,user_id[1]))

        conn.commit()

        cursor.execute("""
            UPDATE accounts SET balance = balance + %s WHERE account_number = %s
        """,(value,account_number))

        conn.commit()
        return True
    
    return False
