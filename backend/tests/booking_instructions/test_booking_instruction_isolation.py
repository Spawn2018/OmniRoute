from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.booking_instruction import BookingInstruction
from tests.sales_invoices.test_sales_invoice_isolation import _booked


@pytest.mark.integration
@pytest.mark.asyncio
async def test_booking_instruction_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="ia")
    row_a = BookingInstruction(
        id=uuid4(),
        organization_id=org_a.id,
        shipment_id=ship_a.id,
        booking_scope="contact_exchange",
        target_role="origin_agent",
        status="suggested",
        source_ref="fixture://booking-instruction/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="ib")
    row_b = BookingInstruction(
        id=uuid4(),
        organization_id=org_b.id,
        shipment_id=ship_b.id,
        booking_scope="ocean",
        target_role="ocean_carrier",
        status="accepted",
        source_ref="fixture://booking-instruction/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(BookingInstruction))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(
        select(BookingInstruction).where(BookingInstruction.id == row_b.id),
    ) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(BookingInstruction))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_booking_instruction_rejects_foreign_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="ix")
    await bind_tenant(session, org_a.id)
    session.add(
        BookingInstruction(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_b.id,
            booking_scope="ocean",
            target_role="ocean_carrier",
            status="suggested",
            source_ref="fixture://booking-instruction/stolen",
            created_by=user_a.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_booking_instruction_list_uses_org_shipment_index(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM booking_instruction "
            "WHERE organization_id = :org_id AND shipment_id = :ship "
            "AND superseded_by IS NULL"
        ),
        {"org_id": org_a.id, "ship": uuid4()},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "ix_booking_instruction_org_shipment" in joined
