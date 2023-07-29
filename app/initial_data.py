import asyncio

from app.db.init_db import init_db
from app.db.session import sessionmanager
from app.core.config import settings


async def create_init_data() -> None:
    async with sessionmanager.session() as session:
        await init_db(session)


async def main() -> None:
    sessionmanager.init(settings.ASYNC_DATABASE_URI)
    await create_init_data()


if __name__ == "__main__":
    asyncio.run(main())
