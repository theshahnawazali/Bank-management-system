from fastapi import APIRouter
from backend.app.schemas.account import UserUpdateBalance, AccountStatus, Transfer
from backend.app.services.bank_service import BankService

router = APIRouter()
# ================================================
#                 BANKING
# ================================================
@router.post('/transactions/deposit',summary="Deposit amount",tags=['Banking'])

async def deposit(
    data : UserUpdateBalance
):
    res = BankService.deposit(
        data.sender_account_number,
        data.amount
    )

    return res

@router.post('/transactions/withdraw',summary="Withdraw amount",tags=['Banking'])
async def deposit(
    data : UserUpdateBalance
):
    res = BankService.withdraw(
        data.sender_account_number,
        data.amount
    )

    return res

@router.post('/transactions/transfer',summary="Transfer amount",tags=['Banking'])
async def transfer(
    data : Transfer
):
    res = BankService.withdraw(
        data.sender_account_number,
        data.amount
    )

    return res


@router.get('/transactions/history',summary="Get all trasaction history of a user",tags=['Banking'])
async def get_all_history(
    data : AccountStatus
):
    res = BankService.get_transaction_history(
        data.account_number
    )

    return res

@router.get('/transactions/{transaction_id}',summary="Get all trasaction history of a user",tags=['Banking'])
async def get_all_history(
    transaction_id : str
):
    res = BankService.get_transaction_id_history(
        transaction_id
    )

    return res
