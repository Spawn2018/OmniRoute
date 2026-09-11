from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.otif_mark import OtifMark


def _mark(
    *,
    organization_id,
    created_by,
    mark_code: str = "otif_pickup_pl",
    scope_kind: str = "pickup",
    source_ref: str = "tenant:manual",
) -> OtifMark:
    return OtifMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        scope_kind=scope_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_otif_mark_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    mark_a = _mark(organization_id=org_a.id, created_by=user_a.id)
    session.add(mark_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    mark_b = _mark(
        organization_id=org_b.id,
        created_by=user_b.id,
        mark_code="otif_delivery_de",
        scope_kind="delivery",
        source_ref="fixture://otif-mark/b",
    )
    session.add(mark_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(OtifMark))).all())
    assert {row.id for row in visible_a} == {mark_a.id}
    hidden = await session.scalar(select(OtifMark).where(OtifMark.id == mark_b.id))
    assert hidden is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_otif_mark_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_mark(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _mark(
            organization_id=org_a.id,
            created_by=user_a.id,
            mark_code="otif_02",
            scope_kind="sku",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_otif_mark_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM otif_mark WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_otif_mark_organization_id" in joined
        or "uq_otif_mark_org_id" in joined
        or "uq_otif_mark_org_source_ref" in joined
        or "uq_otif_mark_org_code" in joined
        or "Index Scan" in joined
    )
