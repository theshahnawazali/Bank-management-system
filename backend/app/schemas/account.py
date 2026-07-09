from pydantic import BaseModel

class UserAccountDetails(BaseModel):
    username : str
    account_type : str
    balance : float
    status : str = "Active"

class UserUpdateBalance(BaseModel):
    sender_account_number : int
    amount : float
    transaction_type : str
    receiver_account_number : int = None
