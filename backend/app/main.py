from services.bank_service import BankService

# print(
#     BankService.deposit(
#         787105308887,
#         500.10
#     )
# )

# print(
#     BankService.withdraw(
#         787105308887,
#         500
#     )
# )

# print(
#     BankService.update_transaction(
#         787105308887,
#         100.23,
#         "Withdraw",
#         "TXN2026070616086",
#         "Success"
#     )
# )

# print(
#     BankService.get_username_by_account_number(
#         787105308887
#     )
# )




# print(
#     BankService.get_balance(
#         787105308887
#     )
# )



# All Import Code are Here

from database.connection import Session, engine
from database.base import Base
from fastapi import FastAPI
from api.auth import router as user_router
from api.bank import router as bank_router

Base.metadata.create_all(engine)

# print(
res = BankService.get_transaction_history(
        787105308887
    )
# )

print(res)
res = list(res)
print(type(res))
app = FastAPI()

app.include_router(user_router)
app.include_router(bank_router)

@app.get('/')
async def root():
    return {
        "message" : "Hello World"
    }

