from typing import Optional

from fastapi import APIRouter, HTTPException, Depends

from src.api.fau import fastapi_users
from src.database import User
from src.database.queries.users import get_users


async def get_optional_user(user: User = Depends(fastapi_users.current_user(optional=True))) -> Optional[User]:
    return user


router = APIRouter()


@router.get("/get-users")
async def get_users_router(
        count: Optional[int] = 10,
        user: Optional[User] = Depends(get_optional_user)):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    else:
        users = await get_users(count=count)
        return users
