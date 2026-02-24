import bank

c1 = ""

while True:
    user = input("User: ").lower()
    print(user)

    if user == "exit":
        print("Exiting....")
        break
    elif user == "create account":
        print("Which type of account you want to open\n Type 1 for Saving Account \n Type 2 for Current Account")
        acc_type = input("Type 1 or 2: ")
        if acc_type == "1" or acc_type == "2":
            name = input("What is your name: ")
            balance = int(input("Amount deposit: "))
            if acc_type == "1":
                bank.saving_acc(name,balance)
                c1 = bank.saving_acc(name,balance)
            else:
                bank.current_acc(name,balance)
                c1 = bank.current_acc(name,balance)
        else:
            print("Invalid Input")
    elif user == "balance":
        if c1 == "":
            print("User not found.Create an account.")
        else:
            bank.check_balance(c1)
    elif user == "withdraw":
        value = int(input("How much money you want to withdraw: "))
        bank.withdraw(c1,value)
    elif user == "deposit":
        bank.deposit(c1,value)
        value = int(input("How much money you want to deposit: "))
    else:
        print("Invalid Input")