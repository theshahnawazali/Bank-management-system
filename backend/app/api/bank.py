from fastapi import APIRouter
from database.dependencies import get_db
from schemas.account import UserAccountDetails
from services.bank_service import BankService

router = APIRouter()

@router.post('/account')
async def create_account(
    user : UserAccountDetails,
    username : str,
    account_type : str,
    balance : float,
    status : str
):
    res = BankService.create_account(
        username,
        account_type,
        balance,
        status
    )

    return res, user

@router.get('/balance')
async def get_balance(
    account_number : int
):
    res = BankService.get_balance(account_number)

    return res

@router.post('/deposit')
async def deposit(
    account_number : int,
    amount : int
):
    pass

@router.post('/trasaction/update')
async def upadate_trasaction(
    account_number : int,
    amount : float,
    transaction_type : str,
    status : str
):
    pass