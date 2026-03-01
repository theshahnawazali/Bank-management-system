from services.auth_service import Signup, Login
from services.bank_service import Deposit, Withdraw, get_account, Transactions
from utils import generator
from models.saving import saving_account 
from models.current import Current_account


# Display available commands menu
print("Type login if you have account\n"
      "Type Signup for creating an new account\n"
      "Type Account to get all information about your account\n"
      "Type withdraw for withdrawing amount\n"
      "Type deposit to deposit amount\n"
      "Type transaction for all transections history\n"
      "Type exit to end the program.")


# Track currently logged-in user
current_user_username = "User"
current_user_name = None


# Main program loop
while True:
    
    # Take command input from user
    user = input(f"{current_user_username}: ").lower()


    # ---------------- USER REGISTRATION ----------------
    if user == "signup":
        name = input("Enter your name: ")

        # Generate unique username
        username = generator.check_username()

        # Take password with minimum length validation
        password = input("Enter Password: ")
        while len(password) < 8:
            print("Password should be minimum 8 character")
            password = input("Enter Password: ")

        # Create new user account
        Signup(name, username, password)

        # Set session user info
        current_user_username = username
        current_user_name = name


        # -------- ACCOUNT TYPE SELECTION --------
        while True:
            type = int(input(
                "Which type of account you want to open\n"
                "Type 1 for Saving Account\n"
                "Type 2 for Current Account"
            ))

            # Validate account type input
            if type == 1 or type == 2:

                # -------- SAVING ACCOUNT --------
                if type == 1:
                    account_number = generator.generate_acc()
                    type = "Saving Account"

                    # Minimum deposit validation
                    balance = int(input("Enter a minimum amount: "))
                    while balance < 0:
                        print("Amount should be positive")
                        balance = int(input("Enter a minimum amount: "))

                    # Create saving account
                    saving_account(current_user_name, type, account_number, balance, current_user_username)
                    current_user_acc_no = account_number

                # -------- CURRENT ACCOUNT --------
                else:
                    account_number = generator.generate_acc()
                    type = "Current Account"

                    balance = int(input("Enter a minimum amount: "))
                    while balance < 0:
                        print("Amount should be positive")
                        balance = int(input("Enter a minimum amount: "))

                    # Create current account
                    Current_account(current_user_name, type, account_number, balance, current_user_username)
                    current_user_acc_no = account_number

                break
            else:
                print("Invalid Output.")


    # ---------------- USER LOGIN ----------------
    elif user == "login":
        username = input("Enter Your Username: ")
        password = input("Enter your Password: ")

        # Authenticate user credentials
        Login(username, password)

        # Update session username
        current_user_username = username
        

    # ---------------- ACCOUNT INFO ----------------
    elif user == "account":

        # Ensure user is logged in before fetching details
        if not current_user_username == "User":
            print("Getting account info....")
            get_account(current_user_username)
        else:
            print("Login First")


    # ---------------- TRANSACTIONS ----------------
    elif user == "withdraw" or user == "deposit" or user == "transaction":

        # Require login before transaction operations
        if not current_user_username == "User":

            # Get transaction amount
            value = int(input("Enter amount: "))

            # Withdraw funds
            if user == "withdraw":
                Withdraw(current_user_username, value)

            # Deposit funds
            elif user == "deposit":
                Deposit(current_user_username, value)

            # Show transaction history
            else:
                Transactions(current_user_username)

        else:
            print("Login First")


    # ---------------- EXIT PROGRAM ----------------
    elif user == "exit":
        current_user_username == "User"
        current_user_name = None
        break


    # ---------------- INVALID COMMAND ----------------
    else:
        print("Invalid Input.")