# Import required modules
import os
import json

# Import account creation service (if needed after signup)
from services.bank_service import Create_Account


# ---------------- BASE USER CLASS ----------------
class User:
    """
    Base User class that stores common user attributes.
    """

    def __init__(self, username, password, name=None):
        # Store basic user credentials
        self.account_no = username
        self.password = password
        self.name = name


# ---------------- SIGNUP CLASS ----------------
class Signup(User):
    """
    Handle new user registration and store user data in JSON file.
    """

    def __init__(self, name, username, password):

        # Initialize parent User class
        super().__init__(name, username, password)

        self.name = name
        self.username = username
        self.password = password

        # Structure new user data
        new_data = {
            self.username: {
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


# ---------------- LOGIN CLASS ----------------
class Login(User):
    """
    Authenticate user credentials against stored JSON data.
    """

    def __init__(self, username, password):

        # Initialize parent User class
        super().__init__(username, password)

        self.username = username
        self.password = password

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