"""Wzorzec testu izolacji tenantów — kopiuj przy każdej nowej tabeli z RLS."""

from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import bind_tenant
from app.models.app_user import AppUser


async def assert_tenant_cannot_read_foreign_row(
    session: AsyncSession,
    tenant_id: UUID,
    foreign_user_id: UUID,
) -> None:
    await bind_tenant(session, tenant_id)
    row = await session.get(AppUser, foreign_user_id)
    assert row is None, "RLS: tenant nie powinien widzieć wiersza innej organizacji"


async def assert_tenant_sees_only_own_rows(
    session: AsyncSession,
    tenant_id: UUID,
    expected_user_ids: set[UUID],
) -> None:
    await bind_tenant(session, tenant_id)
    result = await session.scalars(select(AppUser))
    visible = {row.id for row in result.all()}
    assert visible == expected_user_ids


async def assert_missing_tenant_context_returns_no_rows(session: AsyncSession) -> None:
    await session.execute(text("SELECT set_config('app.current_org', '', true)"))
    result = await session.scalars(select(AppUser))
    assert list(result.all()) == []
