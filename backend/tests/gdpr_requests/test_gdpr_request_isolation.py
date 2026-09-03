from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.gdpr_request import GdprRequest


def _row(*, org, user, kind: str, suffix: str) -> GdprRequest:
    return GdprRequest(
        id=uuid4(),
        organization_id=org.id,
        app_user_id=user.id,
        request_kind=kind,
        status="open",
        source_ref=f"fixture://gdpr-request/{suffix}",
        created_by=user.id,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_gdpr_request_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _row(org=org_a, user=user_a, kind="access", suffix="a")
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _row(org=org_b, user=user_b, kind="erasure", suffix="b")
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(GdprRequest))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(
        select(GdprRequest).where(GdprRequest.id == row_b.id),
    ) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(GdprRequest))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_gdpr_request_rejects_foreign_app_user(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    session.add(
        GdprRequest(
            id=uuid4(),
            organization_id=org_a.id,
            app_user_id=user_b.id,
            request_kind="access",
            status="open",
            source_ref="fixture://gdpr-request/stolen",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()
