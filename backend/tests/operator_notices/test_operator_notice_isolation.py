from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.operator_notice import OperatorNotice


def _unread(*, organization_id, user_id, suffix: str) -> OperatorNotice:
    return OperatorNotice(
        id=uuid4(),
        organization_id=organization_id,
        kind="manual",
        body=f"notatka {suffix}",
        status="unread",
        source_ref=f"fixture://operator-notice/{suffix}",
        created_by=user_id,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_operator_notice_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    row_a = _unread(organization_id=org_a.id, user_id=user_a.id, suffix="a")
    row_b = _unread(organization_id=org_b.id, user_id=user_b.id, suffix="b")

    await bind_tenant(session, org_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(OperatorNotice))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    foreign_b = await session.scalar(
        select(OperatorNotice).where(OperatorNotice.id == row_b.id),
    )
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(OperatorNotice))).all())
    assert {row.id for row in visible_b} == {row_b.id}
