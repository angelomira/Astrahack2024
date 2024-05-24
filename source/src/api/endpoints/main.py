from fastapi import Depends, APIRouter

from src.api.fau import fastapi_users
from src.database import User
from typing import Optional


async def get_optional_user(user: User = Depends(fastapi_users.current_user(optional=True))) -> Optional[User]:
    return user

router = APIRouter()


@router.get("/")
def main_router(user: Optional[User] = Depends(get_optional_user)):
    if user:
        return f"Hello, {user.username}"
    else:
        return f"Hello, everyone!"
