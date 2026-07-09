from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    name : str
    username : str
    email : EmailStr
    password : str
    role : str = "Customer"


class UserLogin(BaseModel):
    username : str
    password : str

class AuthToken(BaseModel):
    username : str
    token : str