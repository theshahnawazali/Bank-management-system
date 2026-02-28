from models.account import Account


class Current_account(Account):
    def __init__(self,name,type,account_no,balance,username):
        super().__init__(type,name,account_no,balance,username)
        self.type = type
        self.name = name
        self.account_number = account_no
        self.username = username
        print("Your Current Account is Open..")