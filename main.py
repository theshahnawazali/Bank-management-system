from services.auth_service import Signup, Login
from services.bank_service import Deposit, Withdraw, get_account, Transactions
from utils import generator
from models.saving import saving_account 
from models.current import Current_account
from utils import validator , hash


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

        # -------- NAME VALIDATION --------
        while True:
            try:
                name = input("Enter your name: ")
                validator.validate_name(name)
                break
            except ValueError as e:
                print(e)

        username = generator.check_username()

        while True:
            try:
                password = input("Enter your password: ")
                validator.validate_password(password)

                secured_password = hash.secure_password(password)

                break
            except ValueError as e:
                print(e)

        # Create new user account
        Signup(name, username, secured_password)

        # Set session user info
        current_user_username = username
        current_user_name = name

        while True:
            try:
                # -------- ACCOUNT TYPE SELECTION --------
                acc_type = int(input(
                    "1 Saving Account\n"
                    "2 Current Account\nChoose: "
                ))

                if acc_type not in [1, 2]:
                    print("Invalid choice")
                    continue

                account_number = generator.generate_acc()

                balance = int(input("Enter initial amount: "))
                validator.validate_initial_balance(balance)

                if acc_type == 1:
                    saving_account(name, "Saving Account", account_number, balance, username)
                else:
                    Current_account(name, "Current Account", account_number, balance, username)

                print("Account Created Successfully")
                break
            except ValueError as e:
                print(e)
                
    elif user == "login":
        # ---------------- USER LOGIN ----------------
        while True:
            try:
                username = input("Enter Your Username: ")
                validator.validate_username(username)

                password = input("Enter your Password: ")
                validator.validate_password(password)
                
                secured_password = hash.secure_password(password)

                # Authenticate user credentials
                Login(username, secured_password)

                # Update session username
                current_user_username = username

                break

            except ValueError as e:
                print(e)
            
            

        
        

    # ---------------- ACCOUNT INFO ----------------
    elif user == "account":

        # Ensure user is logged in before fetching details
        try:
            validator.validate_user_logged_in(current_user_username)
            get_account(current_user_username)

        except PermissionError as e:
            print(e)


    # ---------------- TRANSACTIONS ----------------
    elif user == "withdraw" or user == "deposit":

        # Require login before transaction operations
        try:
            validator.validate_user_logged_in(current_user_username)

            # Get transaction amount
            value = int(input("Enter amount: "))

            # Withdraw funds
            if user == "withdraw":
                Withdraw(current_user_username, value)

            # Deposit funds
            else:
                Deposit(current_user_username, value)
        
        except PermissionError as e:
            print(e)
    
    # ---------------- TRANSACTIONS ----------------
    elif user == "transaction":

        # Show transaction history
        try:
            validator.validate_user_logged_in(current_user_username)
            Transactions(current_user_username)

        except PermissionError as e:
            print(e)



    # ---------------- EXIT PROGRAM ----------------
    elif user == "exit":
        current_user_username == "User"
        current_user_name = None
        break


    # ---------------- INVALID COMMAND ----------------
    else:
        print("Invalid Input.")