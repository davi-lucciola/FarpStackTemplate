from typing import AsyncGenerator
from api.config import settings
from api.utils.logger import ilogger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession


ilogger.info('Starting Database')
engine: AsyncEngine = create_async_engine(settings.DATABASE_URI, echo=settings.SHOW_SQL)


SessionLocal: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = SessionLocal()

    try:
        yield session
    finally:
        await session.close()


ilogger.info('Database Startup Finished')
