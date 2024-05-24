from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional

from src.api.fau import fastapi_users
from src.database import User
from src.database.queries.messages import get_messages, add_new_message
from src.database.queries.users import user_exists_by_id
from pydantic import BaseModel
from loguru import logger

router = APIRouter()


async def get_optional_user(user: User = Depends(fastapi_users.current_user(optional=True))) -> Optional[User]:
    return user


@router.get("/peer/{receiver_id}")
async def get_messages_history(
    receiver_id: int,
    count: Optional[int] = 10,
    user: Optional[User] = Depends(get_optional_user)
):
    logger.info(f"Received request for receiver_id: {receiver_id} with count: {count}")
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not await user_exists_by_id(user_id=receiver_id):
        raise HTTPException(status_code=404, detail="Receiver not found")
    messages = await get_messages(sender_id=user.id, receiver_id=receiver_id, count=count)

    if not messages:
        raise HTTPException(status_code=404, detail="Messages not found")
    return messages


class MessageCreate(BaseModel):
    receiver_id: int
    content: str


@router.post("/peer/{receiver_id}")
async def send_message(message: MessageCreate,
                       user: Optional[User] = Depends(get_optional_user)):
    # Проверка существования receiver_id
    if user is None:
        print(user)
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not await user_exists_by_id(message.receiver_id):
        raise HTTPException(status_code=404, detail="Receiver not found")

    # Проверка существования sender_id (опционально)
    if not await user_exists_by_id(user.id):
        raise HTTPException(status_code=404, detail="Sender not found")

    if await add_new_message(message, user.id):
        print(user)
        return f'Message delivered successfully to {message.receiver_id}'
    else:
        raise HTTPException(status_code=400, detail="Message not delivered")
