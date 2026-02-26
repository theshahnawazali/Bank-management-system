# acc no  Generator
# unique identify

import random
import json
import os

def generate_acc():
    a = random.randint(10000,99999)
    # if os.path.exists("data/user.json"):
    #     with open("data/user.json","r") as f:
    #         try:
    #             data = json.load(f)
    #             for user in data:
    #                 if user["Account Number"] == a:
    #                     generate_acc()
    #                 else:
    #                     pass
    #         except:
    #             print("Error")

    return a