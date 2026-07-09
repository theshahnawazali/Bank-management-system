from fastapi import APIRouter
from database.dependencies import get_db
from schemas.account import UserAccountDetails, UserUpdateBalance
from services.bank_service import BankService

router = APIRouter()

@router.post('/account/create')
async def create_account(
    data : UserAccountDetails,
):
    res = BankService.create_account(
        data.username,
        data.account_type,
        data.balance,
        data.status
    )

    # return data
    if res["status"]:
        return {
            "status" : res['status'],
            "message" : res['message'],
            "data" : data
        }
    
    else:
        return {
            "status" : res['status'],
            "message" : res['message'],
            "data" : data
        }

@router.get('/account/{AccountNumber}')
async def get_account_details(
    AccountNumber : int
):
    result = BankService.get_account_details(
        AccountNumber
    )

    return {
        "name": result.name,
        "username": result.username,
        "email": result.email,
        "balance": result.balance,
        "account_status": result.status,
        "account_created_at": result.created_at,
        "account_type": result.account_type,
    }

@router.get('/balance/{AccountID}')
async def Balance(AccountID : int):
    res = BankService.get_balance({AccountID})
    return res


@router.post('/balance/{Transaction_type}')
async def balance(
    data : UserUpdateBalance,
    Transaction_type : str
):
    method_list = ['deposit', 'withdraw', 'transfer']
    if Transaction_type in method_list:
        res = BankService.UpdateBalance(
            data.sender_account_number,
            data.amount,
            Transaction_type,
            data.receiver_account_number
        )
        return {
            "status" : res['status'],
            "balance" : res['Balance'],
            "transaction id" : res['transaction id'],
            "message" : res["message"]
        }
    
    else:
        return {
            "status" : False,
            "balance" : None,
            "transaction id" : None,
            "message" : "Invalid method"
        }


# to be added soon
@router.get('/transaction/{AccountNumber}')
async def transaction(AccountNumber : int):
    res = BankService.get_transaction_history(AccountNumber)
    # return {
    #     "status" : res["status"],
    #     "message" : res["message"],
    #     "trasactions" : res["trasactions"]
    # }

    return res