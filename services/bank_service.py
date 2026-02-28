import os
import json
from models.account import Account
from models.transaction import Transaction


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





class get_account:
    def __init__(self,username):
        self.username = username

        if os.path.exists("data/user.json"):
            with open("data/user.json","r") as f:
                data = json.load(f)

                for user in data:
                    if self.username in user:
                        if os.path.exists("data/account.json"):
                            with open("data/account.json","r") as a:

                                account_data = json.load(a)

                                for account in account_data:
                                    if self.username in account:
                                        print(f"Name: {account[self.username]["Name"]}")
                                        print(f"Account Number: {account[self.username]["Account Number"]}")
                                        print(f"Balance: {account[self.username]["Balance"]}")
                                        print(f"Account Type: {account[self.username]["Account Type"]}")



class Withdraw:
    def __init__(self,account_username,value):
        self.account_username = account_username
        self.value = value
        self.withdraw()
        
        

    def withdraw(self):
            if not os.path.exists("data/account.json"):
                print("Account file not found")
                return

            with open("data/account.json", "r") as f:
                data = json.load(f)

            for user in data:
                if self.account_username in user:
                    print('Find')
                    Account_no = user[self.account_username]["Account Number"]
                    balance = user[self.account_username]["Balance"]
                    print(balance)
                    if balance >= self.value:
                        balance -= self.value
                        user[self.account_username]["Balance"] = balance

                        with open("data/account.json", "w") as f:
                            json.dump(data, f, indent=4)

                        print("Withdraw successful")
                        print("New Balance:", balance)
                        Transaction(self.account_username,"Debited",self.value,balance)
                    else:
                        print("Insufficient Amount") 


        
class Deposit:
    def __init__(self,account_username,value):
        self.account_username = account_username
        self.value = value
        self.deposit()
        

    def deposit(self):
            if not os.path.exists("data/account.json"):
                print("Account file not found")
                return

            with open("data/account.json", "r") as f:
                data = json.load(f)

            for user in data:
                if self.account_username in user:
                    balance = user[self.account_username]["Balance"]
                    print(balance)
                    if balance > 0:
                        balance += self.value
                        user[self.account_username]["Balance"] = balance

                        with open("data/account.json", "w") as f:
                            json.dump(data, f, indent=4)

                        print("Withdraw successful")
                        print("New Balance:", balance)
                        Transaction(self.account_username,"Debited",self.value,balance)
                    else:
                        print("Insufficient Amount")  

 
class Transactions:
    def __init__(self,username):
        self.account_username = username
        self.transaction()

    def transaction(self):
        if not os.path.exists("data/account.json"):
                print("Account file not found")
                return

        with open("data/account.json", "r") as f:
            data = json.load(f)

        for user in data:
            if self.account_username in user:
                for trans in user[self.account_username]["Transaction"]:
                    print(trans)
            

        



# delete account
class Delete(Account):
    pass




# load account
# save account