from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    name : str
    username : str
    email : EmailStr
    password : str