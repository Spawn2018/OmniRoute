from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.twin_kind import TwinKind
from app.models.twin_mark import TwinMark


def _kind(
    *,
    organization_id,
    created_by,
    kind_code: str,
    source_ref: str,
) -> TwinKind:
    return TwinKind(
        id=uuid4(),
        organization_id=organization_id,
        kind_code=kind_code,
        source_ref=source_ref,
        created_by=created_by,
    )


def _mark(
    *,
    organization_id,
    created_by,
    source_ref: str = "tenant:manual",
    twin_kind: str = "vehicle",
) -> TwinMark:
    return TwinMark(
        id=uuid4(),
        organization_id=organization_id,
        twin_kind=twin_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_twin_mark_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    session.add(
        _kind(
            organization_id=org_a.id,
            created_by=user_a.id,
            kind_code="vehicle",
            source_ref="fixture://twin-kind/a-vehicle",
        )
    )
    await session.flush()
    row_a = _mark(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(
        _kind(
            organization_id=org_b.id,
            created_by=user_b.id,
            kind_code="cargo",
            source_ref="fixture://twin-kind/b-cargo",
        )
    )
    await session.flush()
    row_b = _mark(
        organization_id=org_b.id,
        created_by=user_b.id,
        source_ref="fixture://twin-mark/b",
        twin_kind="cargo",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(TwinMark))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(TwinMark).where(TwinMark.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(TwinMark))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_twin_mark_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        _kind(
            organization_id=org_a.id,
            created_by=user_a.id,
            kind_code="vehicle",
            source_ref="fixture://twin-kind/a-vehicle",
        )
    )
    await session.flush()
    session.add(_mark(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(_mark(organization_id=org_a.id, created_by=user_a.id))
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_twin_mark_fk_rejects_unknown_kind(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(
        _mark(
            organization_id=org_a.id,
            created_by=user_a.id,
            twin_kind="tender",
            source_ref="fixture://twin-mark/missing-kind",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_twin_mark_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    named = await session.execute(
        text(
            "SELECT indexname FROM pg_indexes "
            "WHERE tablename = 'twin_mark' "
            "AND indexname = 'ix_twin_mark_organization_id'"
        ),
    )
    assert named.first() is not None
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM twin_mark WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_twin_mark_organization_id" in joined
        or "uq_twin_mark_org_source_ref" in joined
        or "Index Scan" in joined
    )
