class Bank:
    def __init__(self,name,balance):
        self.name = name
        if balance > 0:
            self.__balance = balance

    def get_balance(self):
        return self.__balance
    
    def withdraw(self,value):
        if value > 0:
            self.value = value
            self.__balance -= self.value
        
    def deposit(self,value):
        if value > 0:
            self.value = value
            self.__balance += self.value

    

class saving_acc(Bank):
    def __init__(self,name,balance):
        super().__init__(name,balance)
        self.account = "Saving Account"
        print("Your Saving Account is Open..")
        print("Your Name: ",self.name)
        print("Account Type: ",self.account )
        print("Total Balance: ",self.get_balance())

class current_acc(Bank):
    def __init__(self, name, balance):
        super().__init__(name, balance)
        self.account = "Current Account"
        print("Your Current Account is Open..")
        print("Your Name: ",self.name)
        print("Account Type: ",self.account )
        print("Total Balance: ",self.get_balance())
        



def check_balance(user):
    print("Total Balance of", user.name,"is",user.get_balance())

def withdraw(user,value):
    print("Amount withdraw from your account: ", value)
    user.withdraw(value)
    check_balance(user)

def deposit(user,value):
    print("Amount deposited to your account: ", value)
    user.deposit(user)
    check_balance(user)