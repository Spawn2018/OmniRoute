from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.tender_decline_reason import TenderDeclineReason


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "tdr_dec_01",
    decline_kind: str = "decline",
    source_ref: str = "fixture://tender-decline-reason/",
) -> TenderDeclineReason:
    return TenderDeclineReason(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        decline_kind=decline_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tender_decline_reason_rls_isolates_tenants(session, two_tenants) -> None:
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
        mark_code="shared_01",
        decline_kind="withdraw",
        source_ref="fixture://tender-decline-reason/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(TenderDeclineReason))).all())
    assert {row.id for row in visible} == {row_a.id}
