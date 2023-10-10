import asyncio
from typing import AsyncGenerator
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app import app
from app.database.core import get_session, engine
from app.database.model import Base
from config import Config


engine_test = create_async_engine(Config.TEST_DB_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.bind = engine_test

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_session] = override_get_async_session

@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_database():
    try:
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except:
        async with engine.begin() as conn:
            await conn.execute(text("COMMIT"))
            await conn.execute(text(f"CREATE DATABASE {Config.TEST_DB_NAME}"))
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        yield ac