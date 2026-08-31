import os
import uuid
from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import bind_tenant
from app.models.app_user import AppUser
from app.models.base import Base
from app.models.organization import Organization

ADMIN_TEST_DATABASE_URL = os.getenv(
    "ADMIN_TEST_DATABASE_URL",
    "postgresql+asyncpg://omniroute:omniroute@localhost:5432/omniroute_test",
)
TENANT_TEST_DATABASE_URL = os.getenv(
    "TENANT_TEST_DATABASE_URL",
    "postgresql+asyncpg://tenant_tester:test@localhost:5432/omniroute_test",
)


async def _apply_rls_policies(conn) -> None:
    await conn.execute(text("ALTER TABLE organization ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE organization FORCE ROW LEVEL SECURITY"))
    await conn.execute(text("DROP POLICY IF EXISTS organization_tenant_isolation ON organization"))
    await conn.execute(
        text(
            """
            CREATE POLICY organization_tenant_isolation ON organization
            USING (id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            """
        ),
    )
    await conn.execute(text("ALTER TABLE app_user ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE app_user FORCE ROW LEVEL SECURITY"))
    await conn.execute(text("DROP POLICY IF EXISTS app_user_tenant_isolation ON app_user"))
    await conn.execute(
        text(
            """
            CREATE POLICY app_user_tenant_isolation ON app_user
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            """
        ),
    )


@pytest_asyncio.fixture
async def engine() -> AsyncGenerator:
    admin_engine = create_async_engine(ADMIN_TEST_DATABASE_URL, pool_pre_ping=True)

    async with admin_engine.begin() as conn:
        await conn.execute(
            text(
                """
                DO $$ BEGIN
                  CREATE ROLE tenant_tester LOGIN PASSWORD 'test' NOINHERIT NOBYPASSRLS;
                EXCEPTION WHEN duplicate_object THEN NULL;
                END $$;
                """
            ),
        )
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await _apply_rls_policies(conn)
        await conn.execute(text("GRANT USAGE ON SCHEMA public TO tenant_tester"))
        await conn.execute(
            text(
                "GRANT SELECT, INSERT, UPDATE, DELETE "
                "ON ALL TABLES IN SCHEMA public TO tenant_tester"
            )
        )

    await admin_engine.dispose()

    test_engine = create_async_engine(TENANT_TEST_DATABASE_URL, pool_pre_ping=True)
    yield test_engine
    await test_engine.dispose()


@pytest_asyncio.fixture
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as db_session:
        yield db_session
        await db_session.rollback()


@pytest_asyncio.fixture
async def two_tenants() -> dict[str, object]:
    admin_engine = create_async_engine(ADMIN_TEST_DATABASE_URL, pool_pre_ping=True)
    org_a = Organization(id=uuid.uuid4(), name="Tenant A", slug=f"tenant-a-{uuid.uuid4().hex[:8]}")
    org_b = Organization(id=uuid.uuid4(), name="Tenant B", slug=f"tenant-b-{uuid.uuid4().hex[:8]}")
    user_a = AppUser(
        id=uuid.uuid4(),
        organization_id=org_a.id,
        email="a@example.com",
        display_name="User A",
    )
    user_b = AppUser(
        id=uuid.uuid4(),
        organization_id=org_b.id,
        email="b@example.com",
        display_name="User B",
    )

    session_factory = async_sessionmaker(admin_engine, expire_on_commit=False)
    async with session_factory() as db_session:
        db_session.add_all([org_a, org_b, user_a, user_b])
        await db_session.commit()

    await admin_engine.dispose()

    return {
        "org_a": org_a,
        "org_b": org_b,
        "user_a": user_a,
        "user_b": user_b,
    }
