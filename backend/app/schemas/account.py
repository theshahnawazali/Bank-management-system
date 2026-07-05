from pydantic import BaseModel

class UserAccountDetails(BaseModel):
    username : str
    account_type : str
    balance : float
    status : str