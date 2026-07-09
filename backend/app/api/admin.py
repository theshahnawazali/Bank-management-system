from fastapi import APIRouter
from schemas.admin import ChangeStatus
from services.admin_service import AdminService

router = APIRouter()

@router.post('/admin/{account_status}')
async def change_bank_account_status(
    account_status : str,
    data : ChangeStatus
):
    res = AdminService.change_bank_account_status(
        data.account_number,
        data.admin_username,
        account_status
    )

    return {
        "status" : res["status"],
        "message" : res["message"]
    }

@router.post('/admin/delete')
async def delete(
    account_number : int
):
    pass