from __future__ import annotations

import time
from typing import List, Dict

from loguru import logger
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from src.database.connection import async_session_factory
from src.database.models import MessagesOrm
import datetime


@logger.catch()
async def add_new_message(data, sender_id) -> bool:
    receiver_id = int(data.receiver_id)
    content = str(data.content)
    timestamp = int(time.time())

    stmt = insert(MessagesOrm).values(sender_id=sender_id,
                                      receiver_id=receiver_id,
                                      content=content,
                                      timestamp=timestamp,
                                      ).on_conflict_do_nothing()
    async with async_session_factory() as session:
        try:
            async with session.begin():
                await session.execute(stmt)

            logger.debug(f'💬 {sender_id} написал {receiver_id} -> {content}')
            return True

        except IntegrityError as err:
            logger.warning(err)
            await session.rollback()
            return False


async def get_messages(sender_id: int, receiver_id: int, count: int) -> List[Dict[str, str]]:
    async with async_session_factory() as session:
        query = select(MessagesOrm.sender_id, MessagesOrm.receiver_id, MessagesOrm.content, MessagesOrm.timestamp).filter(
            or_(
                (MessagesOrm.sender_id == sender_id) & (MessagesOrm.receiver_id == receiver_id),
                (MessagesOrm.sender_id == receiver_id) & (MessagesOrm.receiver_id == sender_id)
            )).limit(count)

        result = await session.execute(query)
        messages = result.fetchall()
    # Преобразование результата в список словарей
    messages_list = [{"sender_id": msg.sender_id,
                      "receiver_id": msg.receiver_id,
                      "content": msg.content,
                      "timestamp": datetime.datetime.utcfromtimestamp(msg.timestamp).strftime('%d-%m-%Y %H:%M:%S UTC')} for msg in messages]
    return messages_list

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
