# =========================================================
# FILE HANDLING
# Centralized File Handling logic for banking system
# =========================================================

import os
import json

from models.transaction import Transaction

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
                            print("Log in successful")
                        else:
                            print("Wrong Password")

                # If username not found in file
                if not found:
                    print("User Not Found")

            except json.JSONDecodeError:
                # Handle invalid JSON format
                print("Invalid Json Format")


# --------------- Create Account Handler ----------------
def create_account_handle(account_no):
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


# --------------- Get Account Handler ----------------
def get_account_handle(username):
    # Check if user file exists
        if os.path.exists("data/user.json"):
            with open("data/user.json", "r") as f:
                data = json.load(f)

                # Find matching user
                for user in data:
                    if username in user:
                        acc_no = str(user[username]["Account Number"])

            
        if os.path.exists("data/account.json"):
            with open("data/account.json", "r") as f:
                data = json.load(f)
            
            for user in data:
                if acc_no in user:
                    print(f"Name: {user[acc_no]['Name']}")
                    print(f"Balance: {user[acc_no]['Balance']}")
                    print(f"Account Type: {user[acc_no]['Account Type']}")
                    print(f"Account Number: {acc_no}")                  


# --------------- Withdraw Handler ----------------
def withdraw_handle(username,value):
    # Check if user file exists
    if os.path.exists("data/user.json"):
        with open("data/user.json", "r") as f:
            data = json.load(f)

            # Find matching user
            for user in data:
                if username in user:
                    acc_no = str(user[username]["Account Number"])

        
    if os.path.exists("data/account.json"):
        with open("data/account.json", "r") as f:
            data = json.load(f)

    # Search for user account
    for user in data:
        if acc_no in user:
            balance = user[acc_no]["Balance"]

            # Check sufficient balance
            if balance >= value:
                balance -= value
                user[acc_no]["Balance"] = balance

                # Save updated balance
                with open("data/account.json", "w") as f:
                    json.dump(data, f, indent=4)

                print("Withdraw successful")
                print("New Balance:", balance)

                # Record transaction log
                Transaction(acc_no, "Debited", value, balance)

            else:
                print("Insufficient Amount")


# --------------- Deposit Handler ----------------
def deposit_handle(username,value):
    # Check if user file exists
    if os.path.exists("data/user.json"):
        with open("data/user.json", "r") as f:
            data = json.load(f)

            # Find matching user
            for user in data:
                if username in user:
                    acc_no = str(user[username]["Account Number"])

        
    if os.path.exists("data/account.json"):
        with open("data/account.json", "r") as f:
            data = json.load(f)

    # Search for user account
    for user in data:
        if acc_no in user:
            balance = user[acc_no]["Balance"]

            # Check sufficient balance
            if balance > 0:
                # Add deposit amount
                balance += value
                user[acc_no]["Balance"] = balance

                # Save updated balance
                with open("data/account.json", "w") as f:
                    json.dump(data, f, indent=4)

                print("Deposit successful")
                print("New Balance:", balance)

                # Record transaction
                Transaction(acc_no, "Credited", value, balance)


# --------------- Transaction Handler ----------------
def transaction_handler(username):
    # Check if user file exists
    if os.path.exists("data/user.json"):
        with open("data/user.json", "r") as f:
            data = json.load(f)

            # Find matching user
            for user in data:
                if username in user:
                    acc_no = str(user[username]["Account Number"])

        
    if os.path.exists("data/account.json"):
        with open("data/account.json", "r") as f:
            data = json.load(f)

        # Print transaction list
        for user in data:
            if acc_no in user:
                for trans in user[acc_no]["Transaction"]:
                    print(trans)

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
    # Check if user file exists
    if os.path.exists("data/user.json"):
        with open("data/user.json", "r") as f:
            data = json.load(f)

            # Find matching user
            for user in data:
                if username in user:
                    acc_no = str(user[username]["Account Number"])

        
    if os.path.exists("data/account.json"):
        with open("data/account.json", "r") as f:
            data = json.load(f)

    # Search for user account
    for user in data:
        if acc_no in user:
            print(user[acc_no]["Balance"])
            balance = user[acc_no]["Balance"]
            # Check sufficient balance
            if balance >= value:
                balance -= value
                user[acc_no]["Balance"] = balance

                # Save updated balance
                with open("data/account.json", "w") as f:
                    json.dump(data, f, indent=4)

                Transaction(acc_no,f"Transfered to {account_number}", value,balance)
                
    if not os.path.exists("data/account.json"):
        print("Account file not found")
        return
    
    with open("data/account.json", "r") as f:
        try:
            data = json.load(f)
        except:
            data = []

    for user in data:
        if account_number in user:
            
            balance = user[account_number]["Balance"]

            if balance > 0:
                # Add deposit amount
                balance += value
                user[account_number]["Balance"] = balance

                # Save updated balance
                with open("data/account.json", "w") as f:
                    json.dump(data, f, indent=4)

                Transaction(account_number,f"Credited from {acc_no}", value,balance)