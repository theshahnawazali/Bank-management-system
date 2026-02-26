import os
import json
from models.account import Account

# create account

class Create_Account:
    def __init__(self,account_no):
        self.account_no = account_no
        
        new_data = {
            account_no : {}
        }

        file_path = "data/account.json"

        # Check file exit or not, if not add 
        if os.path.exists(file_path):
            with open(file_path,"r") as f:
                try:
                    data = json.load(f)
                except:
                    data = []
        
        else:
            data = []

        if isinstance(data,dict):
            data = [data]

        data.append(new_data)

        with open("data/account.json","w") as f:
            json.dump(data, f, indent=4)


# get acc
# class get_account(Account):
#     def get_account(self):
#         return super().get_account()

class get_account:
    def __init__(self,account_number):
        self.account_number = account_number

        if os.path.exists("data/account.json"):
            with open("data/account.json","r") as f:
                data = json.load(f)
                for user in data:
                    if self.account_number in user:
                        print(f"Name: {user[self.account_number]["Name"]}")
                        print(f"Account Number: {self.account_number}")
                        print(f"Balance: {user[self.account_number]["Balance"]}")
                        print(f"Account Type: {user[self.account_number]["Account Type"]}")
                    else:
                        print("Not Found")



# deposit
# class Deposit(Account):
#     def deposit(self, value):
#         return super().deposit(value)
                         
class Withdraw:
    def __init__(self,account_number,value):
        self.account_number = account_number
        self.value = value
        self.withdraw()
        

    def withdraw(self):
            if not os.path.exists("data/account.json"):
                print("Account file not found")
                return

            with open("data/account.json", "r") as f:
                data = json.load(f)

            if self.account_number not in data:
                print("Account not found")
                return

            balance = data[self.account_number]["Balance"]

            if balance >= self.value:
                balance -= self.value
                data[self.account_number]["Balance"] = balance

                with open("data/account.json", "w") as f:
                    json.dump(data, f, indent=4)

                print("Withdraw successful")
                print("New Balance:", balance)
            else:
                print("Insufficient Amount")  
        
class Deposit:
    def __init__(self,account_number,value):
        self.account_number = account_number
        self.value = value
        self.deposit()
        

    def deposit(self):
            if not os.path.exists("data/account.json"):
                print("Account file not found")
                return

            with open("data/account.json", "r") as f:
                data = json.load(f)

            if self.account_number not in data:
                print("Account not found")
                return

            balance = data[self.account_number]["Balance"]

            if balance > 0:
                balance += self.value
                data[self.account_number]["Balance"] = balance

                with open("data/account.json", "w") as f:
                    json.dump(data, f, indent=4)

                print("Withdraw successful")
                print("New Balance:", balance)
            else:
                print("Insufficient Amount")  

 

# delete account
class Delete(Account):
    pass



# # withdraw
# class Withdraw(Account):
#     def withdraw(self, value):
#         return super().withdraw(value)



# load account
# save account