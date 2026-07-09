from pydantic import BaseModel

class ChangeStatus(BaseModel):
    account_number : int
    admin_username : int