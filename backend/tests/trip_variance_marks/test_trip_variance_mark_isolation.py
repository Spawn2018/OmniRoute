from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.trip_variance_mark import TripVarianceMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "var_expected_01",
    variance_kind: str = "expected",
    source_ref: str = "tenant:manual",
) -> TripVarianceMark:
    return TripVarianceMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        variance_kind=variance_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_trip_variance_mark_rls_isolates_tenants(session, two_tenants) -> None:
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
        mark_code="var_gap_b",
        variance_kind="gap",
        source_ref="fixture://trip-variance/b",
    )
    session.add(row_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(TripVarianceMark))).all())
    assert {row.mark_code for row in visible} == {"var_expected_01"}
