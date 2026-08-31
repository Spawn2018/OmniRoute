from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant


def test_refresh_token_model_is_defined_for_tenant_isolation() -> None:
    from app.models.refresh_token import RefreshToken

    assert RefreshToken.__tablename__ == "refresh_token"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_refresh_token_rls_isolates_tenants(session, two_tenants) -> None:
    from app.models.refresh_token import RefreshToken

    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    expires = datetime.now(UTC) + timedelta(days=7)

    row_a = RefreshToken(
        id=uuid4(),
        organization_id=org_a.id,
        user_id=user_a.id,
        token_hash="hash-a",
        expires_at=expires,
        created_by=user_a.id,
    )
    row_b = RefreshToken(
        id=uuid4(),
        organization_id=org_b.id,
        user_id=user_b.id,
        token_hash="hash-b",
        expires_at=expires,
        created_by=user_b.id,
    )

    await bind_tenant(session, org_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(row_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(RefreshToken))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    foreign_b = await session.scalar(select(RefreshToken).where(RefreshToken.id == row_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(RefreshToken))).all())
    assert {row.id for row in visible_b} == {row_b.id}
    foreign_a = await session.scalar(select(RefreshToken).where(RefreshToken.id == row_a.id))
    assert foreign_a is None
