from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.product_ticket import ProductTicket


def _row(
    *,
    organization_id,
    created_by,
    ticket_code: str = "bug_a_01",
    source_ref: str = "tenant:manual",
) -> ProductTicket:
    return ProductTicket(
        id=uuid4(),
        organization_id=organization_id,
        ticket_code=ticket_code,
        title="Login stuck",
        body="Cannot enter after refresh",
        ticket_kind="report",
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_product_ticket_rls_isolates_tenants(
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
        ticket_code="bug_b_02",
        source_ref="fixture://product-ticket/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(ProductTicket))).all())
    assert {row.id for row in visible_a} == {row_a.id}

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(ProductTicket))).all())
    assert {row.id for row in visible_b} == {row_b.id}
