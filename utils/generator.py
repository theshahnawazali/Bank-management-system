import random
import json
import os
from utils import validator

# Generate a unique account number and verify it is unique

def generate_acc():
    a = random.randint(10000,99999)
    if os.path.exists("data/account.json"):
        with open("data/account.json","r") as f:
            try:
                data = json.load(f)
                for user in data:
                    if str(a) in user:
                        generate_acc()
                    else:
                        pass
                    
            except:
                print("Error")

    return a

# Ensure the username is unique
def check_username():
    username = input("Enter an unique Username: ").lower()
    while len(username) < 4:
        print("Username should be minimum 4 charecter")
        username = input("Enter an unique Username: ").lower()
    # check_unique = validator.validate_username(username)

    # if check_unique == True:
    #     print("Yes username is unique.")
    # else:
    #     print("False")


    if os.path.exists("data/user.json"):
        with open("data/user.json","r") as f:
            try:
                data = json.load(f)
                for user in data:
                    if username in user:
                        print("Username already exits. Try another.")
                        check_username()
                    else:
                        pass
            except:
                print("Error")

    return username