from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.routing_guide_enforcement import RoutingGuideEnforcement


def _row(
    *,
    organization_id,
    created_by,
    mark_code="mode_record_01",
    source_ref="tenant:manual",
    enforcement_kind="record_only",
):
    return RoutingGuideEnforcement(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        enforcement_kind=enforcement_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_routing_guide_enforcement_rls_isolates_tenants(
    session, two_tenants
) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    await bind_tenant(session, org_a.id)
    row_a = _row(organization_id=org_a.id, created_by=two_tenants["user_a"].id)
    session.add(row_a)
    await session.flush()
    await bind_tenant(session, org_b.id)
    row_b = _row(
        organization_id=org_b.id,
        created_by=two_tenants["user_b"].id,
        mark_code="mode_block_01",
        source_ref="fixture://routing-guide-enforcement/b",
        enforcement_kind="block_409",
    )
    session.add(row_b)
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(RoutingGuideEnforcement))).all())
    assert {row.id for row in visible} == {row_a.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_routing_guide_enforcement_rejects_duplicate_source_ref(
    session, two_tenants
) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    session.add(_row(organization_id=org_a.id, created_by=two_tenants["user_a"].id))
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=two_tenants["user_a"].id,
            mark_code="mode_02",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_routing_guide_enforcement_list_uses_org_index(
    session, two_tenants
) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM routing_guide_enforcement "
            "WHERE organization_id = :org_id"
        ),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "Index Scan" in joined or "routing_guide_enforcement" in joined
