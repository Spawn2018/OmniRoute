from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.memory_edge import MemoryEdge


def _link(
    *,
    organization_id,
    created_by,
    source_ref: str = "tenant:manual",
    edge_kind: str = "recalls",
) -> MemoryEdge:
    return MemoryEdge(
        id=uuid4(),
        organization_id=organization_id,
        edge_kind=edge_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_memory_edge_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _link(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _link(
        organization_id=org_b.id,
        created_by=user_b.id,
        source_ref="fixture://memory-edge/b",
        edge_kind="blocks",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(MemoryEdge))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(MemoryEdge).where(MemoryEdge.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(MemoryEdge))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_memory_edge_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_link(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(_link(organization_id=org_a.id, created_by=user_a.id))
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_memory_edge_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    named = await session.execute(
        text(
            "SELECT indexname FROM pg_indexes "
            "WHERE tablename = 'memory_edge' "
            "AND indexname = 'ix_memory_edge_organization_id'"
        ),
    )
    assert named.first() is not None
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM memory_edge WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_memory_edge_organization_id" in joined
        or "uq_memory_edge_org_source_ref" in joined
        or "Index Scan" in joined
    )
