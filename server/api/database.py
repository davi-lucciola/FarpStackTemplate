from typing import AsyncGenerator
from api.config import settings
from api.utils.logger import ilogger
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import create_engine, Engine


ilogger.info('Starting Database')

engine: Engine = create_engine(settings.DATABASE_URI, echo=settings.SHOW_SQL)

SessionLocal: Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=Session,
    bind=engine,
)

async def get_db() -> AsyncGenerator[Session, None]:
    session: Session = SessionLocal()

    try:
        yield session
    finally:
        session.close()

ilogger.info('Database Startup Finished')
