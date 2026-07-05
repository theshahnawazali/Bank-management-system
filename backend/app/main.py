# from fastapi import FastAPI

# router = FastAPI()

# @router.get('/')
# async def root():
#     return {"Msg" : True}



# from models.account import Account
# from models.account import Account
from database.base import Base
from models.account import Account
from models.transaction import Transaction
from models.user import User
from models.sessions import Session
from database.connection import engine, Session

from database.dependencies import get_db

session = Session()


Base.metadata.create_all(bind=engine)

# user = session.query(User).all()

# for u in user:
#     print(u.user_id, u.email)

from services.auth_service import UserService



# result = UserService.Register(
#     "shahnawaz ali",
#     "gsfjg",
#     "jsf",
#     "jfsgja"
# )

from services.bank_service import BankService

# result = BankService.create_account(
#     1,
#     "current",
#     120.25,
#     "active"
# ) 

# result = UserService.Login(
#     "shahnawaz",
#     '123456'
# )

# print(result)


# print(
#     BankService.create_account(
#         "jsf",
#         "Current",
#         122.20,
#         "Active"
#     )
# )
# print(
#     UserService.Register(
#         "Shahnawaz Ali",
#         "theshahnawazali@gmail.com",
#         "shahnawazali",
#         "Shahnawaz"
#     )
# )

# print(
#     BankService.create_account(
#         "shahnawazali",
#         "Saving",
#         500.00,
#         "Active"
#     )
# )

# print(
#     BankService.get_current_user(
#         295768493905
#     )
# )










# All Import Code are Here

from database.connection import Session, engine
from database.base import Base
from fastapi import FastAPI
from api.auth import router as user_router
from api.bank import router as bank_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(bank_router)

@app.get('/')
async def root():
    return {
        "message" : "Hello World"
    }

