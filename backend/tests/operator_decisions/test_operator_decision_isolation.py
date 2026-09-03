from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.operator_decision import OperatorDecision


def _pending(*, organization_id, user_id, subject_id, suffix: str) -> OperatorDecision:
    return OperatorDecision(
        id=uuid4(),
        organization_id=organization_id,
        subject_kind="inbound_message",
        subject_id=subject_id,
        status="pending",
        source_ref=f"fixture://operator-decision/{suffix}",
        created_by=user_id,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_operator_decision_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    shared_subject = uuid4()

    row_a = _pending(
        organization_id=org_a.id,
        user_id=user_a.id,
        subject_id=shared_subject,
        suffix="a",
    )
    row_b = _pending(
        organization_id=org_b.id,
        user_id=user_b.id,
        subject_id=shared_subject,
        suffix="b",
    )

    await bind_tenant(session, org_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(OperatorDecision))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    foreign_b = await session.scalar(
        select(OperatorDecision).where(OperatorDecision.id == row_b.id),
    )
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(OperatorDecision))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_operator_decision_pending_unique_per_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    subject_id = uuid4()

    await bind_tenant(session, org_a.id)
    session.add(
        _pending(
            organization_id=org_a.id,
            user_id=user_a.id,
            subject_id=subject_id,
            suffix="first",
        )
    )
    await session.flush()
    session.add(
        _pending(
            organization_id=org_a.id,
            user_id=user_a.id,
            subject_id=subject_id,
            suffix="dup",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()
