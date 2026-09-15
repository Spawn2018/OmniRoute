from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.impact_edge_mark import ImpactEdgeMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "ship_to_inv",
    from_kind: str = "shipment",
    to_kind: str = "inventory",
    source_ref: str = "tenant:manual",
) -> ImpactEdgeMark:
    return ImpactEdgeMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        from_kind=from_kind,
        to_kind=to_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_impact_edge_mark_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _row(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _row(
        organization_id=org_b.id,
        created_by=user_b.id,
        mark_code="rev_to_cash",
        from_kind="revenue",
        to_kind="cash",
        source_ref="fixture://impact-edge-mark/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(ImpactEdgeMark))).all())
    assert {row.id for row in visible} == {row_a.id}
