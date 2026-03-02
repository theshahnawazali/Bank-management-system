# Import required modules
import os
import json
from utils import file_handler

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

        file_handler.signup_handle(self.username,self.name,self.password)


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

        file_handler.login_handle(self.username,self.password)
        