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

from backend.app.database.dependencies import get_db
from pydantic import EmailStr
from backend.app.services.auth_service import AuthService

router = APIRouter()

# =========================================================================
#               AUTHENTICATION
# =========================================================================
@router.post('/auth/register',summary="Register User",tags=["Authentication"])
async def register(
    data : UserRegister,
    db = Depends(get_db)
):
    res = AuthService.register(
        db,
        data.name,
        data.email,
        data.username,
        data.password,
        data.role
    )

    return res

@router.post('/auth/verify-email',summary="Verify Email", tags=["Authentication"])
async def verify_email(
    data : OTP
):
    res = AuthService.verify_email(
        data.username,
        data.otp
    )

    return res

@router.post('/auth/login',summary="Login",tags=["Authentication"])
async def login(
    data : UserLogin
):
    res =AuthService.login(
        data.username,
        data.password
    )

    return res
@router.post('/auth/verify-login-otp',summary="Verify Login otp",tags=['Authentication'])
async def verify_login_otp(
    data : OTP
):
    res = AuthService.verify_login_otp(
        data.username,
        data.otp
    )

    return res

@router.post('/auth/logout',summary='Logout User',tags=["Authentication"])
async def logout(
    data : UserLogout
):
    res = AuthService.Logout(
        data.username,
        data.token
    )

    return res

@router.post('/auth/forget-password',summary="Forget Password",tags=["Authentication"])
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

@router.post("/auth/verify-reset-otp",summary="Verify Reset password",tags=['Authentication'])
async def verify_reset_otp(
    data : OTP
):
    res = AuthService.verify_otp(
        data.username,
        data.otp
    )
    return res

@router.post("/auth/reset-password",summary="Reset Password",tags=['Authentication'])
async def reset_password(
    data : ResetPassword
):
    res = AuthService.reset_password(
        data.username,
        data.password,
        data.new_password
    )

    return res

@router.get('auth/{username}',summary="Will be implement in future",tags=['Authentication'])
async def get_me(
    username : str
):
    pass
