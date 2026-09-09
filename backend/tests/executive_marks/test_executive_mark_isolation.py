from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.executive_mark import ExecutiveMark


def _brief(
    *,
    organization_id,
    created_by,
    source_ref: str = "tenant:manual",
    question_kind: str = "loss",
) -> ExecutiveMark:
    return ExecutiveMark(
        id=uuid4(),
        organization_id=organization_id,
        question_kind=question_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_executive_mark_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _brief(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _brief(
        organization_id=org_b.id,
        created_by=user_b.id,
        source_ref="fixture://executive-mark/b",
        question_kind="risk",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(ExecutiveMark))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(ExecutiveMark).where(ExecutiveMark.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(ExecutiveMark))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_executive_mark_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_brief(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(_brief(organization_id=org_a.id, created_by=user_a.id))
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_executive_mark_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    named = await session.execute(
        text(
            "SELECT indexname FROM pg_indexes "
            "WHERE tablename = 'executive_mark' "
            "AND indexname = 'ix_executive_mark_organization_id'"
        ),
    )
    assert named.first() is not None
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM executive_mark WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_executive_mark_organization_id" in joined
        or "uq_executive_mark_org_source_ref" in joined
        or "Index Scan" in joined
    )
