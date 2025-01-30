from contextlib import asynccontextmanager
import logging
from conf import DSN
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.engine = create_async_engine(DSN, echo=True, future=True)

    async def ping_database(self):
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("Successfully connected to the Database!")
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async_session = async_sessionmaker(self.engine, class_=AsyncSession)
        session = None
        try:
            session = async_session()
            async with session:
                yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

    async def close_database(self):
        await self.engine.dispose()
        logger.info("Database connection closed!")


database = Database()


async def setup_database():
    await database.ping_database()
    await database.create_tables()
