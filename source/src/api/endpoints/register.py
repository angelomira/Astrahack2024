import asyncio
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from src.database.queries.users import add_new_user, user_exists
from typing import Optional
router = APIRouter()


class MessageRequest(BaseModel):
    username: str
    password: str
    email: str


@router.post("/register/")
async def reg_account(data: MessageRequest, request: Request):
    try:
        client_ip = request.headers.get('X-Forwarded-For')
        if client_ip is None:
            client_ip = request.client.host

        client_port = request.client.port

        if await user_exists(data.username):
            response = f'User with username {data.username} already exists!'
            return {"response": response}

        else:
            await add_new_user(data)
            response = f'Success registration with username: {data.username}'
            return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
