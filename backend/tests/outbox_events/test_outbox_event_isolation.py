from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.outbox_event import OutboxEvent


def _event(*, organization_id, user_id, suffix: str, subject_id=None) -> OutboxEvent:
    return OutboxEvent(
        id=uuid4(),
        organization_id=organization_id,
        event_kind="inbound_message_saved",
        subject_id=subject_id or uuid4(),
        status="pending",
        source_ref=f"outbox://inbound-message/{suffix}",
        created_by=user_id,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_outbox_event_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    shared = uuid4()
    row_a = _event(organization_id=org_a.id, user_id=user_a.id, suffix="a", subject_id=shared)
    row_b = _event(organization_id=org_b.id, user_id=user_b.id, suffix="b", subject_id=shared)

    await bind_tenant(session, org_a.id)
    session.add(row_a)
    await session.flush()
    await bind_tenant(session, org_b.id)
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(OutboxEvent))).all())
    assert {row.id for row in visible_a} == {row_a.id}

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(OutboxEvent))).all())
    assert {row.id for row in visible_b} == {row_b.id}

    dup = _event(organization_id=org_a.id, user_id=user_a.id, suffix="dup", subject_id=shared)
    await bind_tenant(session, org_a.id)
    session.add(dup)
    with pytest.raises(IntegrityError):
        await session.flush()
