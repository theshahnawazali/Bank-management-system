from fastapi import APIRouter
from schemas.auth import UserRegister
from database.dependencies import get_db
from pydantic import EmailStr
from services.auth_service import UserService

router = APIRouter()

# ==================== POST Method for user Register ====================
@router.post('/register')
async def RegisterUser(
    user : UserRegister,
    name : str,
    email : EmailStr,
    username : str,
    password : str,
    role : str = "Customer"

):
    res = UserService.Register(
        name,
        email,
        username,
        password,
        role
    )

    if res["status"]:
        return {
            "status" : res["status"],
            "message" : res["message"],
            "data" : user
        }
    
    else:
        return {
            "status" : res["status"],
            "message" : res["message"],
            "data" : user
        }



# ================= POST Method for user Login =======================
@router.post("/login")
async def userlogin(
    user : UserRegister,
    username : str,
    password : str
):
    res = UserService.Login(
        username,
        password
    )

    if res["status"] == False:
        return {
            "status" : res["status"],
            "message" : res["message"],
            "data" : user
        }
    
    else:
        return {
            "status" : res["status"],
            "message" : res["message"],
            "data" : user
        }