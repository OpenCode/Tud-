import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
from app import app # FastAPI app
from models import Base
from db import get_db
from pytest_asyncio import fixture as async_fixture


# Database for test purposes only
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


# -----------------
# 1. Database Setup
# -----------------

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    return engine


@pytest.fixture(scope="session")
def setup_db(test_engine):
    """
        Create tables before tests and drop them after tests.
    """
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def test_session(test_engine, setup_db):
    """Crea una sessione di database transazionale per ogni test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionTesting()
    yield session
    # Remove (rollback) all the data craeted during the test
    session.close()
    transaction.rollback()
    connection.close()


# ------------------------------
# 2. Override Dependency FastAPI
# ------------------------------

@pytest.fixture(scope="function")
def override_db_dependency(test_session):
    """Dependency che restituisce la sessione di test."""
    def override_get_db():
        try:
            yield test_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    return app


# ------------------------------
# 3. Aync API client for testing
# ------------------------------

@async_fixture(scope="function")
async def client(override_db_dependency):
    async with AsyncClient(
        transport=ASGITransport(app=override_db_dependency),
        base_url="http://test"
    ) as c:
        yield c
