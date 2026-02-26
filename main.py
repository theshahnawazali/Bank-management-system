from services.auth_service import Signup,Login
from services.bank_service import Create_Account , Deposit, Withdraw, Delete, get_account
from utils import generator
from models.saving  import saving_account 
from models.current import Current_account

print("Type login if you have account\nType Signup for creating an new account")

current_user_username = "User"
current_user_name = None

# get_account("52761")
# Deposit("52761",1000)
# Withdraw("28210",100)
Withdraw("28210",100)
Deposit("28210",500)




while False:
    user = input(f"{current_user_username}: ").lower()

    if user == "signup":
        name = input("Enter your name: ")
        username = generator.check_username()
        password = input("Enter Password: ")
        while len(password) < 8:
            print("Password should be minimum 8 charecter")
            password = input("Enter Password: ")

        
        Signup(name,username,password)
        current_user_username = username
        current_user_name = name
        # type = int(input("Which type of account you want to open\n Type 1 for Saving Account \nType 2 fo Current Account"))
        while True:
            type = int(input("Which type of account you want to open\n Type 1 for Saving Account \nType 2 fo Current Account"))

            if type == 1 or type == 2:
                if type == 1:
                    account_number = generator.generate_acc()
                    type = "Saving Account"
                    balance = int(input("Enter an minimum amount: "))
                    while balance < 0:
                        print("Amount Should be in Positive")
                        balance = int(input("Enter an minimum amount: "))
                    saving_account(current_user_name,type,account_number,balance)
                else:
                    account_number = generator.generate_acc()
                    type = "Current Account"
                    balance = int(input("Enter an minimum amount: "))
                    while balance < 0:
                        print("Amount Should be in Positive")
                        balance = int(input("Enter an minimum amount: "))
                    Current_account(current_user_name,type,account_number,balance)

                break
            else:
                print("Invalid Output.")
    
    elif user == "login":
        username = input("Enter Your Username: ")
        password = input("Enter your Password: ")
        Login(username,password)
        current_user_username = username

    elif user == "account":
        print("Getting account info....")
        get_account()

        
    elif user == "exit":
        break

    else:
        print("Invalid Input.")


    