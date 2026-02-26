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
class get_account(Account):
    def get_account(self):
        return super().get_account()


# deposit
class Deposit(Account):
    def deposit(self, value):
        return super().deposit(value)


# delete account
class Delete(Account):
    pass



# withdraw
class Withdraw(Account):
    def withdraw(self, value):
        return super().withdraw(value)



# load account
# save account