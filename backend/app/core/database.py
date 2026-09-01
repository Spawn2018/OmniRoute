import asyncio
from collections.abc import AsyncGenerator
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

_READY_TIMEOUT_SECONDS = 2.0


async def probe_database() -> bool:
    try:
        async with asyncio.timeout(_READY_TIMEOUT_SECONDS):
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
    except (TimeoutError, OSError, SQLAlchemyError):
        return False
    return True


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def bind_tenant(session: AsyncSession, organization_id: UUID) -> None:
    await session.execute(
        text("SELECT set_config('app.current_org', :org_id, true)"),
        {"org_id": str(organization_id)},
    )
