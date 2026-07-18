import re
from fastapi import HTTPException
from fastapi import APIRouter, Depends
from backend.app.schemas.auth import (
    UserLogin,
    UserLogout,
    UserRegister,
    OTP,
    AuthToken,
    ForgetPassword,
    ResetPassword
)
from fastapi.responses import JSONResponse
from backend.app.database.dependencies import get_db
from pydantic import EmailStr
from backend.app.services.auth_service import AuthService
from backend.app.core.security import create_session_token, generete_random_otp
from backend.app.database.connection import redis_conn


router = APIRouter(tags=["Authentication"])

# =========================================================================
#               AUTHENTICATION
# =========================================================================
@router.post('/auth/register',summary="Register User")
async def register(
    data : UserRegister
):
    if not all([
        data.name.strip(),
        data.email.strip(),
        data.username.strip(),
        data.password.strip(),
        data.role.strip(),
    ]):
        return JSONResponse(
            status_code=422,
            content={
                "details" : "Missing feild required"
            }
        )
    
    if re.search(r"[<>;'\"`]|--", data.username):
        raise HTTPException(
            status_code=422,
            detail="Invalid characters in name"
        )
    
    res = AuthService.register(
        data.name,
        data.email,
        data.username,
        data.password,
        data.role
    )

    if res['status']:
        token = create_session_token({
            "username" : data.username,
            "role" : data.role
        })

        generete_random_otp(data.username)
        
        return {
            "token" : token,
            "token_type" : "bearer",
            "data" : res
        }

@router.post('/auth/verify-email',summary="Verify Email")
async def verify_email(
    data : OTP
):
    res = AuthService.verify_email(
        data.username,
        data.otp
    )

    return res

@router.post('/auth/otp')
async def otp(
    data : OTP
):
    otp = generete_random_otp(
        data.username
    )

    return True

@router.post('/auth/login',summary="Login")
async def login(
    data : UserLogin
):
    if not all([
        data.username.strip(),
        data.password.strip()
    ]):
        return JSONResponse(
            status_code=422,
            content={
                "details" : "Missing feild required"
            }
        )
    
    res =AuthService.login(
        data.username,
        data.password
    )

    if res["status"]:
        token = create_session_token({
            "username" : data.username,
            "role" : res["role"]
        })

        return {
            "token" : token,
            "token_type": "bearer",
            "data" : res
        }
        
@router.post('/auth/verify-login-otp',summary="Verify Login otp")
async def verify_login_otp(
    data : OTP
):
    res = AuthService.verify_login_otp(
        data.username,
        data.otp
    )

    return res

@router.post('/auth/logout',summary='Logout User')
async def logout(
    data : UserLogout
):
    res = AuthService.Logout(
        data.username,
        data.token
    )

    return res

@router.post('/auth/forget-password',summary="Forget Password")
async def forget_password(
    data : ForgetPassword,
    db = Depends(get_db)
):
    res = AuthService.forget_password(
        db,
        data.username,
        data.new_password
    )
    return res

@router.post("/auth/verify-reset-otp",summary="Verify Reset password")
async def verify_reset_otp(
    data : OTP
):
    res = AuthService.verify_otp(
        data.username,
        data.otp
    )
    return res

@router.post("/auth/reset-password",summary="Reset Password")
async def reset_password(
    data : ResetPassword
):
    res = AuthService.reset_password(
        data.username,
        data.password,
        data.new_password
    )

    return res

@router.get('auth/{username}',summary="Will be implement in future")
async def get_me(
    username : str
):
    pass
