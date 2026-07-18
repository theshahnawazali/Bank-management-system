# All Import Code are Here
from backend.app.database.connection import SessionLocal, engine
from backend.app.database.base import Base
from backend.app.models.account import Account
from backend.app.models.requests import Request
from backend.app.models.transaction import Transaction
from backend.app.models.user import User
from backend.app.models.audit import Audit
from fastapi import FastAPI , HTTPException
from fastapi import Request as API_Request
from fastapi.responses import JSONResponse
from backend.app.core.security import verify_session_token
from backend.app.api.auth import router as user_router
from backend.app.api.account import router as account_router
from backend.app.api.admin import router as admin_router
from backend.app.api.banking import router as bank_router
from backend.app.middlerware.middleware import Middlerware
# from backend.app.middlerware.middleware_logging import RequestLoggingMiddleware
from backend.app.exceptions import (
    UsernameAlreadyExists,
    UsernameNotExists,
    EmailAlreadyExists,
    EmailNotExists,
    RedisConnectionError,
    TokenSetUnsuccesfull,
    IncorrectPassword,
    BankAccountAlreadyExist,
    NegativeBalance,
    BankAccountNotExists,
    AccountNotActive,
    InsufficientBalance,
    TemporaryLock
)


from backend.app.services.bank_service import BankService
from backend.app.services.admin_service import AdminService
from backend.app.services.auth_service import AuthService

Base.metadata.create_all(engine)


app = FastAPI()

app.include_router(user_router)
app.include_router(bank_router)
app.include_router(admin_router)
app.include_router(account_router)

app.add_middleware(Middlerware)
# app.add_middleware(RequestLoggingMiddleware)
# ================== Middlewares =========================

# print(
#     # verify_session_token(
#     #     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R1c2VyMyIsInJvbGUiOiJBZG1pbiIsImV4cCI6MTc4NDE0Mjg5OH0.hp2h4NPkCk63HkT_FBgZikMX7a9j-JXR5oC9bjeBrTM"
#     # ),
#     BankService.deposit(
#         879315081979,
#         7946.26
#     )
# )

# ============== Custom Exceptions ========================
@app.exception_handler(UsernameNotExists)
async def usernamenotexist(
    request : API_Request,
    exc : UsernameNotExists
):
    return JSONResponse(
        status_code=409,
        content={
            "details" : str(exc)
        }
    )

@app.exception_handler(EmailNotExists)
async def usernamenotexist(
    request : API_Request,
    exc : EmailNotExists
):
    return JSONResponse(
        status_code=409,
        content={
            "details" : str(exc)
        }
    )

@app.exception_handler(UsernameAlreadyExists)
async def username_handler(
    request : API_Request,
    exc : UsernameAlreadyExists
):
    return JSONResponse(
        status_code=409,
        content={
            "details" : str(exc),
            "field" : "username"
        }
    )

@app.exception_handler(EmailAlreadyExists)
async def email_handler(
    request : API_Request,
    exc : EmailAlreadyExists
):
    return JSONResponse(
        status_code=409,
        content={
            "details" : str(exc),
            "field" : "Email"
        }
    )

@app.exception_handler(TokenSetUnsuccesfull)
async def token_unsuccessful(
    request : API_Request,
    exc : TokenSetUnsuccesfull
):
    return JSONResponse(
        status_code=409,
        content={
            "details" : str(exc)
        }
    )

@app.exception_handler(RedisConnectionError)
async def redis_connection(
    request : API_Request,
    exc : RedisConnectionError
):
    return JSONResponse(
        status_code=409,
        content={
            "details" : str(exc)
        }
    )

@app.exception_handler(IncorrectPassword)
async def incorrect_password(
    request : API_Request,
    exc : IncorrectPassword
):
    return JSONResponse(
        status_code=409,
        content={
            "details" : str(exc)
        }
    )

@app.exception_handler(BankAccountAlreadyExist)
async def account_exits(
    request : API_Request,
    exc : BankAccountAlreadyExist
):
    return JSONResponse(
        status_code=409,
        content={
            "details" : str(exc)
        }
    )

@app.exception_handler(NegativeBalance)
async def negative_balanace(
    request : API_Request,
    exc : NegativeBalance
):
    return JSONResponse(
        status_code=409,
        content={
            "details" : str(exc)
        }
    )

@app.exception_handler(BankAccountNotExists)
async def account_not_exist(
    request : API_Request,
    exc : BankAccountNotExists
):
    return JSONResponse(
        status_code=409,
        content={
            "details" : str(exc)
        }
    )

@app.exception_handler(AccountNotActive)
async def account_not_active(
    request : API_Request,
    exc : AccountNotActive
):
    return JSONResponse(
        status_code=409,
        content={
            "details" : str(exc)
        }
    )

@app.exception_handler(InsufficientBalance)
async def sameaccount(
    request : API_Request,
    exc : InsufficientBalance
):
    return JSONResponse(
        status_code=409,
        content={
            "details" :str(exc)
        }
    )

@app.exception_handler(TemporaryLock)
async def sameaccount(
    request : API_Request,
    exc : TemporaryLock
):
    return JSONResponse(
        status_code=409,
        content={
            "details" :str(exc)
        }
    )

@app.exception_handler(ValueError)
async def value_error(
    request : API_Request,
    exc : ValueError
):
    return JSONResponse(
        status_code=409,
        content={
            "details" :str(exc)
        }
    )

@app.get('/')
async def root():
    return {
        "message" : "FastAPI connection successfull"
    }
