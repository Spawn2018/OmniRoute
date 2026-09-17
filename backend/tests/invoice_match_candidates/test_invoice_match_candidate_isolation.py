from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.invoice_match_candidate import InvoiceMatchCandidate


def _row(
    *,
    organization_id,
    created_by,
    candidate_code: str = "cand_01",
    candidate_kind: str = "proposed",
    source_ref: str = "tenant:manual",
) -> InvoiceMatchCandidate:
    return InvoiceMatchCandidate(
        id=uuid4(),
        organization_id=organization_id,
        candidate_code=candidate_code,
        candidate_kind=candidate_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_invoice_match_candidate_rls_isolates_tenants(session, two_tenants) -> None:
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
        candidate_code="cand_02",
        candidate_kind="held",
        source_ref="fixture://invoice-match-candidate/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(InvoiceMatchCandidate))).all())
    assert {row.id for row in visible} == {row_a.id}
