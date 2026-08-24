import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./rbac_test.db"

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.dependencies import get_db
from app.main import app
from app.models import Base


@pytest.fixture(autouse=True)
async def setup_db():
    engine = create_async_engine("sqlite+aiosqlite:///./rbac_test.db", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(autouse=True)
def override_db():
    engine = create_async_engine("sqlite+aiosqlite:///./rbac_test.db", echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def _override():
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()
