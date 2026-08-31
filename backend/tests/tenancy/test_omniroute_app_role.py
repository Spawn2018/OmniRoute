from urllib.parse import urlparse

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import Settings
from tests.conftest import ADMIN_TEST_DATABASE_URL


def test_runtime_database_url_default_is_omniroute_app() -> None:
    default_url = Settings.model_fields["database_url"].default
    assert isinstance(default_url, str)
    parsed = urlparse(default_url)
    assert parsed.username == "omniroute_app"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_omniroute_app_role_has_no_bypassrls(engine: object) -> None:
    assert engine is not None
    admin = create_async_engine(ADMIN_TEST_DATABASE_URL, pool_pre_ping=True)
    try:
        async with admin.connect() as conn:
            row = (
                await conn.execute(
                    text(
                        "SELECT rolsuper, rolbypassrls FROM pg_roles "
                        "WHERE rolname = 'omniroute_app'"
                    )
                )
            ).one_or_none()
        assert row is not None, "rola omniroute_app musi istnieć (migracja 005 / conftest)"
        assert row.rolsuper is False
        assert row.rolbypassrls is False
    finally:
        await admin.dispose()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_omniroute_app_without_org_sees_no_rows(
    engine: object, two_tenants: dict[str, object]
) -> None:
    assert engine is not None
    assert two_tenants["user_a"] is not None
    app_url = ADMIN_TEST_DATABASE_URL.replace(
        "://omniroute:", "://omniroute_app:", 1
    )
    app_engine = create_async_engine(app_url, pool_pre_ping=True)
    try:
        async with app_engine.connect() as conn:
            await conn.execute(text("SELECT set_config('app.current_org', '', true)"))
            count = (await conn.execute(text("SELECT count(*) FROM app_user"))).scalar_one()
        assert count == 0
    finally:
        await app_engine.dispose()
