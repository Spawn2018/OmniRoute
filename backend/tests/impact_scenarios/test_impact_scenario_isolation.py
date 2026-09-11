from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.impact_scenario import ImpactScenario


def _row(
    *,
    organization_id,
    created_by,
    scenario_code: str = "stock_to_sales_01",
    source_ref: str = "tenant:manual",
) -> ImpactScenario:
    return ImpactScenario(
        id=uuid4(),
        organization_id=organization_id,
        scenario_code=scenario_code,
        chain_label="stock to sales",
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_impact_scenario_rls_isolates_tenants(session, two_tenants) -> None:
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
        scenario_code="sales_to_ebitda_02",
        source_ref="fixture://impact-scenario/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(ImpactScenario))).all())
    assert {row.id for row in visible} == {row_a.id}
