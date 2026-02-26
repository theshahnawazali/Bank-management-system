import json
import os

class Account:
    def __init__(self,name,type,account_number,balance):   # Name 
        self.__account_number = account_number    #account number
        self.__balance = balance  # balance
        self.type = type
        self.name = name

        new_data = {
            self.__account_number : {
                "Name" : self.name, 
                "Balance": self.__balance,
                "Account Type": self.type,
                "Transaction": []
            }
            
        }

        file_path = "data/account.json"

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
        

    def get_account(self):
        return self.name, self.__account_number, self.__balance

    def deposit(self,value):
        if value > 0:
            self.__balance += value

    def withdraw(self,value):
        if value <= self.__balance:
            self.__balance -= value

    

    



    

        








# deposits
# withdraw
# get balance