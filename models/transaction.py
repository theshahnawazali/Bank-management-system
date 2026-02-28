# transaction time
# amount
# timestamp
import os
import json
from datetime import datetime




def current_time():
    now = datetime.now()
    formatted = now.strftime("%d-%m-%Y %H:%M:%S")
    return formatted

class Transaction:
    def __init__(self,account_username,trans_type,amount, total):
        self.account_username = account_username
        self.trans_type = trans_type
        self.amount =amount
        self.total = total
        self.transacton()

    def transacton(self):
        if not os.path.exists("data/account.json"):
                print("Account file not found")
                return
        
        with open("data/account.json","r") as f:
            data = json.load(f)

        for user in data:
                if self.account_username in user:
                    Account_no = user[self.account_username]["Account Number"]
                    balance = user[self.account_username]["Balance"]

                    user[self.account_username]["Transaction"].append(f"{current_time()} ---> {self.trans_type} amount is {self.amount} Total {self.total}")
                    
                    with open("data/account.json","w") as f:
                        json.dump(data, f, indent=4)

        # if self.account_no not in data:
        #             print("Account not found")
        #             return
        
        


        
        

