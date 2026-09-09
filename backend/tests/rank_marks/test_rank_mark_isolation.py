from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.rank_mark import RankMark


def _axis(
    *,
    organization_id,
    created_by,
    source_ref: str = "tenant:manual",
    rank_kind: str = "price",
) -> RankMark:
    return RankMark(
        id=uuid4(),
        organization_id=organization_id,
        rank_kind=rank_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rank_mark_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _axis(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _axis(
        organization_id=org_b.id,
        created_by=user_b.id,
        source_ref="fixture://rank-mark/b",
        rank_kind="carbon",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(RankMark))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    hidden = select(RankMark).where(RankMark.id == row_b.id)
    assert await session.scalar(hidden) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(RankMark))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rank_mark_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_axis(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(_axis(organization_id=org_a.id, created_by=user_a.id))
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rank_mark_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    named = await session.execute(
        text(
            "SELECT indexname FROM pg_indexes "
            "WHERE tablename = 'rank_mark' "
            "AND indexname = 'ix_rank_mark_organization_id'"
        ),
    )
    assert named.first() is not None
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM rank_mark WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_rank_mark_organization_id" in joined
        or "uq_rank_mark_org_source_ref" in joined
        or "Index Scan" in joined
    )
