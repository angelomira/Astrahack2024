from typing import Annotated

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import BigInteger, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base

user_id_unique = Annotated[int, mapped_column(BigInteger, unique=True)]
chat_id_unique = Annotated[int, mapped_column(BigInteger, unique=True)]

user_id_pk = Annotated[int, mapped_column(BigInteger, primary_key=True)]
user_id_fk = Annotated[int, mapped_column(BigInteger, ForeignKey("users.id"))]
chat_id_fk = Annotated[int, mapped_column(BigInteger, ForeignKey("chats.chat_id"))]

chat_id_pk_fk = Annotated[int, mapped_column(BigInteger, ForeignKey("chats.chat_id"), primary_key=True)]

user_nick_uniq = Annotated[str, mapped_column(unique=True)]

id_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
id_uniq = Annotated[int, mapped_column(unique=True)]

bigint = Annotated[int, mapped_column(BigInteger)]


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    id: Mapped[id_pk]
    username: Mapped[str] = mapped_column(String(length=50), unique=True, nullable=None)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=None)
    email: Mapped[str] = mapped_column(String(length=256), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[bigint]
    last_auth: Mapped[bigint]


class MessagesOrm(Base):
    __tablename__ = "messages"
    id: Mapped[id_pk]
    sender_id: Mapped[user_id_fk]
    receiver_id: Mapped[user_id_fk]
    content: Mapped[str]
    timestamp: Mapped[bigint]


class ActivityOrm(Base):
    __tablename__ = "activity"
    id: Mapped[id_pk]
    user_id: Mapped[user_id_fk]
    type: Mapped[str]
    timestamp: Mapped[bigint]
