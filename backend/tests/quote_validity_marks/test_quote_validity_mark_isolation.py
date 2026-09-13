from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.quote_validity_mark import QuoteValidityMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "qvm_open_main",
    validity_kind: str = "open",
    source_ref: str = "fixture://quote-validity-mark/",
) -> QuoteValidityMark:
    return QuoteValidityMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        validity_kind=validity_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_quote_validity_mark_rls_isolates_tenants(session, two_tenants) -> None:
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
        mark_code="qvm_revised_sub",
        validity_kind="revised",
        source_ref="fixture://quote-validity-mark/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(QuoteValidityMark))).all())
    assert {row.id for row in visible} == {row_a.id}
