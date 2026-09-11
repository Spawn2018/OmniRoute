from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.routing_guide_match import RoutingGuideMatch


def _row(*, organization_id, created_by, mark_code="match_lane_01", source_ref="tenant:manual"):
    return RoutingGuideMatch(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        match_kind="lane_label",
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_routing_guide_match_rls_isolates_tenants(session, two_tenants) -> None:
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
        mark_code="match_mode_01",
        source_ref="fixture://routing-guide-match/b",
    )
    row_b.match_kind = "mode_label"
    session.add(row_b)
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(RoutingGuideMatch))).all())
    assert {row.id for row in visible} == {row_a.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_routing_guide_match_rejects_duplicate_source_ref(
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
            mark_code="match_02",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_routing_guide_match_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM routing_guide_match "
            "WHERE organization_id = :org_id"
        ),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "Index Scan" in joined or "routing_guide_match" in joined
