from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.cost_to_serve import CostToServe
from tests.parties.test_customer_sop_isolation import _sop
from tests.sales_invoices.test_sales_invoice_isolation import _booked


async def _noted(session, *, org, user, sop_id, quotation_id, suffix: str) -> CostToServe:
    row = CostToServe(
        id=uuid4(),
        organization_id=org.id,
        customer_sop_id=sop_id,
        quotation_id=quotation_id,
        source_ref=f"fixture://cost-to-serve/{suffix}",
        created_by=user.id,
    )
    session.add(row)
    await session.flush()
    return row


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cost_to_serve_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="sa")
    sop_a = _sop(
        organization_id=org_a.id,
        party_id=ship_a.party_id,
        code="pack_sa",
        created_by=user_a.id,
    )
    session.add(sop_a)
    await session.flush()
    row_a = await _noted(
        session,
        org=org_a,
        user=user_a,
        sop_id=sop_a.id,
        quotation_id=ship_a.quotation_id,
        suffix="a",
    )

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="sb")
    sop_b = _sop(
        organization_id=org_b.id,
        party_id=ship_b.party_id,
        code="pack_sb",
        created_by=user_b.id,
    )
    session.add(sop_b)
    await session.flush()
    row_b = await _noted(
        session,
        org=org_b,
        user=user_b,
        sop_id=sop_b.id,
        quotation_id=ship_b.quotation_id,
        suffix="b",
    )

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(CostToServe))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(CostToServe).where(CostToServe.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(CostToServe))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cost_to_serve_rejects_foreign_sop(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="xb")
    sop_b = _sop(
        organization_id=org_b.id,
        party_id=ship_b.party_id,
        code="pack_xb",
        created_by=user_b.id,
    )
    session.add(sop_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="xa")
    session.add(
        CostToServe(
            id=uuid4(),
            organization_id=org_a.id,
            customer_sop_id=sop_b.id,
            quotation_id=ship_a.quotation_id,
            source_ref="fixture://cost-to-serve/stolen",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()
