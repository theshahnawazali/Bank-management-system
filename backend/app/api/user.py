from fastapi import APIRouter

router = APIRouter()

# ==========================================================
#                     USERS
# ==========================================================
@router.get('/users/profile/{username}')
async def user_profile(
    username :str
):
    pass