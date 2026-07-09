# All Import Code are Here
from database.connection import SessionLocal, engine
from database.base import Base
from models.account import Account
from models.requests import Request
from models.transaction import Transaction
from models.user import User
from fastapi import FastAPI
from api.auth import router as user_router
from api.bank import router as bank_router


from services.bank_service import BankService
from services.admin_service import AdminService
from services.auth_service import AuthService

Base.metadata.create_all(engine)


app = FastAPI()

app.include_router(user_router)
app.include_router(bank_router)

@app.get('/')
async def root():
    return {
        "message" : "Hello World"
    }


from utils.id_generator import generate_otp

# print(generate_otp())

# print(
#     AuthService.create_and_send_otp("shahnawazali")
# )

# print(
#     AuthService.verify_otp(
#         "shahnawazali",
#         352338
#     )
# )
import time 
start = time.time()

# print(
#     AuthService.register(
#         "Shahnawaz Ali",
#         "shahnawaz@gmail.com",
#         "shahnawaz",
#         "password"
#     )
# )

print(
    # AuthService.verify_register_otp(
    #     "shahnawaz",
    #     "123456"
    # )

    AuthService.register(
        "Shahnawaz Ali",
        "shahnawazali@gmail.com",
        "shahnawaz",
        "password"
    )
)

end = time.time()

print(end - start)