from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.routing_guide import RoutingGuide


def _guide(
    *,
    organization_id,
    created_by,
    guide_code: str = "guide_pl_de",
    source_ref: str = "tenant:manual",
) -> RoutingGuide:
    return RoutingGuide(
        id=uuid4(),
        organization_id=organization_id,
        guide_code=guide_code,
        lane_label=None,
        mode_label=None,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_routing_guide_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    guide_a = _guide(organization_id=org_a.id, created_by=user_a.id)
    session.add(guide_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    guide_b = _guide(
        organization_id=org_b.id,
        created_by=user_b.id,
        guide_code="guide_de_pl",
        source_ref="fixture://routing-guide/b",
    )
    session.add(guide_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(RoutingGuide))).all())
    assert {row.id for row in visible_a} == {guide_a.id}
    hidden = await session.scalar(select(RoutingGuide).where(RoutingGuide.id == guide_b.id))
    assert hidden is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_routing_guide_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    session.add(_guide(organization_id=org_a.id, created_by=user_a.id))
    await session.flush()
    session.add(
        _guide(
            organization_id=org_a.id,
            created_by=user_a.id,
            guide_code="guide_02",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_routing_guide_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM routing_guide WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_routing_guide_organization_id" in joined
        or "uq_routing_guide_org_id" in joined
        or "uq_routing_guide_org_source_ref" in joined
        or "uq_routing_guide_org_code" in joined
        or "Index Scan" in joined
    )
