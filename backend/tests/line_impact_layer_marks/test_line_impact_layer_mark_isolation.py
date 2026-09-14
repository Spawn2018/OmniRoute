from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.line_impact_layer_mark import LineImpactLayerMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "lil_scored_01",
    layer_kind: str = "scored",
    source_ref: str = "tenant:manual",
) -> LineImpactLayerMark:
    return LineImpactLayerMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        layer_kind=layer_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_line_impact_layer_mark_rls_isolates_tenants(
    session,
    two_tenants,
) -> None:
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
        mark_code="lil_forecast_02",
        layer_kind="forecast",
        source_ref="fixture://line-impact-layer/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(LineImpactLayerMark))).all())
    assert {row.id for row in visible_a} == {row_a.id}

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(LineImpactLayerMark))).all())
    assert {row.id for row in visible_b} == {row_b.id}
