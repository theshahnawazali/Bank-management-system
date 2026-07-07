from fastapi import APIRouter
from schemas.auth import UserRegister, UserLogin
from database.dependencies import get_db
from pydantic import EmailStr
from services.auth_service import UserService

router = APIRouter()

# ==================== POST Method for user Register ====================
@router.post('/register')
async def RegisterUser(
    data : UserRegister
):
    res = UserService.Register(
        data.name,
        data.email,
        data.username,
        data.password,
        data.role
    )

    if res["status"]:
        return {
            "status" : res["status"],
            "message" : res["message"],
            "role" : data.role,
            "data" : data
        }
    
    else:
        return {
            "status" : res["status"],
            "message" : res["message"],
            "data" : data
        }


# ================= POST Method for user Login =======================
@router.post("/login")
async def userlogin(
    data : UserLogin
):
    res = UserService.Login(
        data.username,
        data.password
    )

    if res["status"] == False:
        return {
            "status" : res["status"],
            "message" : res["message"],
            "role" : res["role"],
            "data" : data
        }
    
    else:
        return {
            "status" : res["status"],
            "message" : res["message"],
            "role" : res["role"],
            "data" : data
        }