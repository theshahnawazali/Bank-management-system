from fastapi import APIRouter
from backend.app.database.dependencies import get_db
from backend.app.schemas.account import (
    AccountStatus,
    UserAccountDetails
)
from backend.app.services.bank_service import BankService

router = APIRouter()


@router.get('/accounts',summary="Get all accounts details",tags=["Accounts"])
async def get_all_account():
    res = BankService.get_all_accounts()

    return res

@router.post('/accounts/create',summary="Open your bank account",tags=["Accounts"])
async def create_account(
    data : UserAccountDetails
):
    res = BankService.create_account(
        data.username,
        data.account_type,
        data.balance,
        data.status
    )

    return res

@router.get('/account/{AccountNumber}',summary="Get account number details",tags=["Accounts"])
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

@router.get('/accounts/{account_number}/balance',summary='Get user balance',tags=['Accounts'])
async def get_balance(
    account_number : int
):
    res = BankService.get_balance(
        account_number
    )

    return res

@router.put('/accounts/{account_number}/freeze',summary="Freeze Accounts",tags=['Accounts'])
async def freeze_account(
    data : AccountStatus
):
    res = BankService.freeze_account(
        data.account_number
    )

    return res

@router.put('accounts/{account_number}/unfreeze',summary="Unfreeze Accounts",tags=['Accounts'])
async def unfreeze_account(
    data : AccountStatus
):
    res = BankService.unfreeze_account(
        data.account_number
    )

    return res

@router.get('/accounts/trasactions',summary="Get all Transaction history",tags=['Admin'])
async def get_all_transaction_history():
    res = BankService.get_all_transaction_history()

    return res
