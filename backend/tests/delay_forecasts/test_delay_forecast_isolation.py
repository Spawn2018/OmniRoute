from uuid import uuid4
from decimal import Decimal

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.delay_forecast import DelayForecast


def _row(*, organization_id, created_by, forecast_code: str = "late_24h_01", source_ref: str = "tenant:manual") -> DelayForecast:
    return DelayForecast(
        id=uuid4(),
        organization_id=organization_id,
        forecast_code=forecast_code,
        horizon_hours=24,
        p_late=Decimal("0.3500"),
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delay_forecast_rls_isolates_tenants(session, two_tenants) -> None:
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
        forecast_code="late_6h_de",
        source_ref="fixture://delay-forecast/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(DelayForecast))).all())
    assert {row.id for row in visible} == {row_a.id}
