from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.counterfactual_run import CounterfactualRun


def _row(
    *,
    organization_id,
    created_by,
    source_ref: str = "fixture://counterfactual-run/",
    run_code: str = "fuel_spike",
) -> CounterfactualRun:
    return CounterfactualRun(
        id=uuid4(),
        organization_id=organization_id,
        run_code=run_code,
        baseline_label="plan z wczoraj",
        levers_label="paliwo w gore",
        result_label="eta plus dwie godziny",
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_counterfactual_run_rls_isolates_tenants(session, two_tenants) -> None:
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
        run_code="port_close",
        source_ref="fixture://counterfactual-run/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(CounterfactualRun))).all())
    assert {row.id for row in visible} == {row_a.id}
