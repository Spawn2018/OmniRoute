from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.position_event import PositionEvent


def _row(
    *,
    organization_id,
    created_by,
    event_code: str = "pos_yard_01",
    source_kind: str = "gps",
    source_ref: str = "tenant:manual",
) -> PositionEvent:
    return PositionEvent(
        id=uuid4(),
        organization_id=organization_id,
        event_code=event_code,
        source_kind=source_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_position_event_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _row(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _row(
        organization_id=org_b.id,
        created_by=user_b.id,
        event_code="pos_gate_02",
        source_kind="manual",
        source_ref="fixture://position-event/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(PositionEvent))).all())
    assert {row.id for row in visible} == {row_a.id}
