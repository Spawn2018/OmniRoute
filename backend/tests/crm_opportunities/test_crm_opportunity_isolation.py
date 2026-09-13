from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.crm_opportunity import CrmOpportunity


def _row(
    *,
    organization_id,
    created_by,
    opportunity_code: str = "opp_acme_01",
    stage_kind: str = "open",
    source_ref: str = "tenant:manual",
) -> CrmOpportunity:
    return CrmOpportunity(
        id=uuid4(),
        organization_id=organization_id,
        opportunity_code=opportunity_code,
        stage_kind=stage_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_crm_opportunity_rls_isolates_tenants(session, two_tenants) -> None:
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
        opportunity_code="opp_beta_lost",
        stage_kind="lost",
        source_ref="fixture://crm-opportunity/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(CrmOpportunity))).all())
    assert {row.id for row in visible} == {row_a.id}
