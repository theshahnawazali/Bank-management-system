# All Import Code are Here
from backend.app.database.connection import SessionLocal, engine
from backend.app.database.base import Base
from backend.app.models.account import Account
from backend.app.models.requests import Request
from backend.app.models.transaction import Transaction
from backend.app.models.user import User
from backend.app.models.audit import Audit
from fastapi import FastAPI
from backend.app.api.auth import router as user_router
from backend.app.api.bank import router as bank_router


from backend.app.services.bank_service import BankService
from backend.app.services.admin_service import AdminService
from backend.app.services.auth_service import AuthService

Base.metadata.create_all(engine)


app = FastAPI()

app.include_router(user_router)
app.include_router(bank_router)

@app.get('/')
async def root():
    return {
        "message" : "Hello World"
    }


from backend.app.utils.id_generator import generate_otp

# =============== Test Login =====================

print(
    AuthService.login(
        "shahnawaz",
        "password"
    ),

    AuthService.login(
        "shahnawaz",
        "incorrect",
    ),
    AuthService.login(
        "gjhskjl",
        "fghjl"
    )
)

print(
    BankService.get_balance(
        1
    )
)