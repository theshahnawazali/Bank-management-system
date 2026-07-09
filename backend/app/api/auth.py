from fastapi import APIRouter
from schemas.auth import UserRegister, UserLogin, AuthToken
from database.dependencies import get_db
from pydantic import EmailStr
from services.auth_service import AuthService

router = APIRouter()

# ==================== POST Method for user register ====================
@router.post('/register')
async def RegisterUser(
    data : UserRegister
):
    res = AuthService.register(
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


# ================= POST Method for user login =======================
@router.post("/login")
async def userlogin(
    data : UserLogin
):
    res = AuthService.login(
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
    
# ============== verify token =================
@router.post('/login/verify')
async def verify_token(
    data : AuthToken
):
    res = AuthService.verify_session_token(
        data.username,
        data.token
    )

    return res