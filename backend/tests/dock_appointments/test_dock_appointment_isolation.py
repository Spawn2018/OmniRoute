from datetime import date, time
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.dock_appointment import DockAppointment
from app.models.location import Location
from app.models.stop import Stop
from tests.sales_invoices.test_sales_invoice_isolation import _booked


def _zone(*, organization_id, created_by, code: str, name: str) -> Location:
    return Location(
        id=uuid4(),
        organization_id=organization_id,
        kind="postal_zone",
        name=name,
        code=code,
        source_ref="tenant:manual",
        created_by=created_by,
    )


def _halt(*, organization_id, created_by, shipment_id, location_id) -> Stop:
    return Stop(
        id=uuid4(),
        organization_id=organization_id,
        shipment_id=shipment_id,
        location_id=location_id,
        stop_kind="unloading",
        sequence_no=1,
        time_zone="Europe/Warsaw",
        status="pending",
        source_ref="fixture://stop/dock",
        created_by=created_by,
    )


def _advice(*, organization_id, created_by, shipment_id, stop_id, code: str) -> DockAppointment:
    return DockAppointment(
        id=uuid4(),
        organization_id=organization_id,
        shipment_id=shipment_id,
        stop_id=stop_id,
        appointment_code=code,
        appointment_status="advised",
        window_date=date(2026, 9, 9),
        window_start_local=time(8, 0, 0),
        window_end_local=time(10, 0, 0),
        source_ref="fixture://dock-appointment/iso",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_dock_appointment_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="da")
    loc_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-DA", name="DA")
    session.add(loc_a)
    await session.flush()
    halt_a = _halt(
        organization_id=org_a.id,
        created_by=user_a.id,
        shipment_id=ship_a.id,
        location_id=loc_a.id,
    )
    session.add(halt_a)
    await session.flush()
    row_a = _advice(
        organization_id=org_a.id,
        created_by=user_a.id,
        shipment_id=ship_a.id,
        stop_id=halt_a.id,
        code="dock_a",
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="db")
    loc_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="PL-DB", name="DB")
    session.add(loc_b)
    await session.flush()
    halt_b = _halt(
        organization_id=org_b.id,
        created_by=user_b.id,
        shipment_id=ship_b.id,
        location_id=loc_b.id,
    )
    session.add(halt_b)
    await session.flush()
    row_b = _advice(
        organization_id=org_b.id,
        created_by=user_b.id,
        shipment_id=ship_b.id,
        stop_id=halt_b.id,
        code="dock_b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(DockAppointment))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert (
        await session.scalar(select(DockAppointment).where(DockAppointment.id == row_b.id)) is None
    )

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(DockAppointment))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_dock_appointment_rejects_foreign_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="dx")
    loc_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="PL-DX", name="DX")
    session.add(loc_b)
    await session.flush()
    halt_b = _halt(
        organization_id=org_b.id,
        created_by=user_b.id,
        shipment_id=ship_b.id,
        location_id=loc_b.id,
    )
    session.add(halt_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    session.add(
        _advice(
            organization_id=org_a.id,
            created_by=user_a.id,
            shipment_id=ship_b.id,
            stop_id=halt_b.id,
            code="stolen",
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_dock_appointment_rejects_stop_off_route(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]

    await bind_tenant(session, org_a.id)
    ship_one = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="d1")
    ship_two = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="d2")
    loc = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-D2", name="D2")
    session.add(loc)
    await session.flush()
    halt_two = _halt(
        organization_id=org_a.id,
        created_by=user_a.id,
        shipment_id=ship_two.id,
        location_id=loc.id,
    )
    session.add(halt_two)
    await session.flush()
    session.add(
        _advice(
            organization_id=org_a.id,
            created_by=user_a.id,
            shipment_id=ship_one.id,
            stop_id=halt_two.id,
            code="off_route",
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_dock_appointment_list_uses_org_stop_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM dock_appointment "
            "WHERE organization_id = :org_id AND stop_id = :stop_id"
        ),
        {"org_id": org_a.id, "stop_id": uuid4()},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "ix_dock_appointment_org_stop" in joined
