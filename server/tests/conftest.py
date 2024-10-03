import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import AsyncGenerator, Generator
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from api import create_app
from api.models import IBaseModel
from api.database import get_db


DATABASE_URL = 'sqlite:///:memory:'
test_engine = create_async_engine(
    DATABASE_URL,
    connect_args={
        'check_same_thread': False
    },
    poolclass=StaticPool
)

TestSession: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=test_engine,
)

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    db: AsyncSession = TestSession(bind=test_engine, autocommit=False)
    
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def test_lifespan(app: FastAPI):
    IBaseModel.metadata.create_all(bind=test_engine)
    yield
    IBaseModel.metadata.drop_all(bind=test_engine)


test_app = create_app(test_lifespan)
test_app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='module')
def test_client() -> Generator[TestClient, None, None]:
    with TestClient(test_app) as test_client:
        yield test_client
