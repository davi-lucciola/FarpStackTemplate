import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import AsyncGenerator, Generator
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.pool import StaticPool

from api import create_app
from api.models import IBaseModel
from api.database import get_db
from api.user.user_model import User
from api.user.user_repository import UserRepository


DATABASE_URL = 'sqlite:///:memory:'

test_engine: Engine = create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool
)

TestSessionLocal: Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=Session,
    bind=test_engine,
)

async def override_test_db() -> AsyncGenerator[Session, None]:
    session: Session = TestSessionLocal()

    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope='module')
def test_db() -> Generator[Session, None, None]:
    session: Session = TestSessionLocal()
    yield session
    session.close() 


@pytest.fixture(scope='module')
def user_repository(test_db: Session):
    return UserRepository(test_db)


@pytest.fixture(scope='module')
def test_app(user_repository: UserRepository):
    IBaseModel.metadata.create_all(bind=test_engine)

    admin_user = User('Admin', 'admin@email.com', '1234')
    user_repository.save(admin_user)

    test_app = create_app()
    test_app.dependency_overrides[get_db] = override_test_db

    yield test_app

    IBaseModel.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope='module')
def client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)

