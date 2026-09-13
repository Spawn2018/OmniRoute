from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.tracking_consent import TrackingConsent


def _row(
    *,
    organization_id,
    created_by,
    consent_code: str = "cns_party_01",
    consent_kind: str = "party",
    source_ref: str = "tenant:manual",
) -> TrackingConsent:
    return TrackingConsent(
        id=uuid4(),
        organization_id=organization_id,
        consent_code=consent_code,
        consent_kind=consent_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tracking_consent_rls_isolates_tenants(session, two_tenants) -> None:
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
        consent_code="cns_driver_02",
        consent_kind="driver",
        source_ref="fixture://tracking-consent/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(TrackingConsent))).all())
    assert {row.id for row in visible} == {row_a.id}
