from __future__ import annotations

import time
from typing import List, Dict

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from loguru import logger
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import async_session_factory, get_async_session
from src.database.models import User


@logger.catch()
async def add_new_user(data) -> bool:
    username = str(data.username)
    password = str(data.password)
    email = str(data.email)
    created_at = int(time.time())
    last_auth = int(time.time())

    stmt = insert(User).values(username=username,
                               password=password,
                               email=email,
                               created_at=created_at,
                               last_auth=last_auth
                               ).on_conflict_do_nothing()
    async with async_session_factory() as session:
        try:
            async with session.begin():
                await session.execute(stmt)

            logger.debug(f'✅👤 Пользователь {username} успешно добавлен в базу.')
            return True

        except IntegrityError as err:
            logger.warning(err)
            await session.rollback()
            return False


async def user_exists(username: str) -> bool:
    async with async_session_factory() as session:
        query = select(User.username).filter_by(username=username).limit(1)
        result = await session.execute(query)

    user = result.scalar_one_or_none()
    return bool(user)


async def user_exists_by_id(user_id: str) -> bool:
    async with async_session_factory() as session:
        query = select(User.username).filter_by(id=user_id).limit(1)
        result = await session.execute(query)

    user = result.scalar_one_or_none()
    return bool(user)


async def get_users(count: int) -> List[Dict[str, str]]:
    async with async_session_factory() as session:
        query = select(User.id, User.username).limit(count)
        result = await session.execute(query)
        messages = result.fetchall()
    # Преобразование результата в список словарей
    users_list = [{"id": user.id, "username": user.username} for user in messages]
    return users_list


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

# async def get_level(session: AsyncSession, user_id: int) -> int:
#     query = select(UsersOrm.level).filter_by(user_id=user_id).limit(1)
#     result = await session.execute(query)
#
#     level = result.scalar()
#
#     return level
#
#
# async def get_exp(session: AsyncSession, user_id: int) -> int:
#     query = select(UsersOrm.exp).filter_by(user_id=user_id).limit(1)
#     result = await session.execute(query)
#
#     exp = result.scalar()
#
#     return exp
#
#
# async def get_nick(session: AsyncSession, user_id: int) -> str:
#     query = select(UsersOrm.nick).filter_by(user_id=user_id).limit(1)
#     result = await session.execute(query)
#
#     nick = result.scalar()
#
#     return nick
#
#
# async def get_language_code(message: Message) -> str:
#     """Gets user language code from message."""
#     language_code = message.from_user.language_code
#     return language_code
