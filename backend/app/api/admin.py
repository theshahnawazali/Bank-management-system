from fastapi import APIRouter
from backend.app.schemas.admin import ChangeStatus
from backend.app.services.admin_service import AdminService
from backend.app.services.auth_service import AuthService

router = APIRouter()

@router.get('/admin/users',summary="Get all users",tags=['Admin'])
async def get_all_user():
    res = AuthService.get_all_users()

    return res

@router.get('/admin/user/{username}',summary="Get user by username",tags=['Admin'])
async def get_user_by_username(
    username : str
):
    res = AuthService.get_user_by_username(
        username
    )

    return res

