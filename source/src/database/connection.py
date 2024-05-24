from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config.config_reader import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=settings.DEBUG,
)

async_session_factory = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


Base = declarative_base()


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        logger.info("Creating tables...")
        try:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tables created successfully.")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")

