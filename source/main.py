import asyncio
from src.api.server import run_server
from src.database.connection import create_db_and_tables


async def main():
    await create_db_and_tables()
    await run_server()


if __name__ == '__main__':
    asyncio.run(main())
