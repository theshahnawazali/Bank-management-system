from fastapi import APIRouter
from schemas.auth import UserRegister
from database.dependencies import get_db
from pydantic import EmailStr
from services.auth_service import UserService

router = APIRouter()

@router.post('/register')
async def RegisterUser(
    user : UserRegister,
    name : str,
    email : EmailStr,
    username : str,
    password : str

):
    return UserService.Register(
        name,
        email,
        username,
        password
    ), user

@router.post("/login")
async def userlogin(
    user : UserRegister,
    username : str,
    password : str
):
    status = UserService.Login(
        username,
        password
    )

    return status, user