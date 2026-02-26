import os
import json
from services.bank_service import Create_Account

class User:
    def __init__(self,username,password,name=None):
        self.account_no = username
        self.password = password
        self.name = name

        

class Signup(User):
    def __init__(self,username, password,name):
        super().__init__(name,username, password)
        self.name = name
        self.username = username
        self.password = password


        new_data = {
            self.username : {
                "Name": self.name,
                "Password": self.password
            }
            
        }

        file_path = "data/user.json"

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

        with open("data/user.json","w") as f:
            json.dump(data, f, indent=4)


class Login(User):
    def __init__(self,username, password):
        super().__init__(username, password)
        self.username = username
        self.password = password
        
        file_path = "data/user.json"
        found = False

        if os.path.exists(file_path):
            with open(file_path,"r") as f:
                try:
                    data = json.load(f)
                    for user in data:
                        if username in user:
                            if user[username]["Password"] == password:
                                print("Log in successful")
                            else:
                                print("Wrong Password")
                            found = True

                        if not found:
                            print("User Not Found")
    
                except json.JSONDecodeError:
                    print("Invalid Json Format")