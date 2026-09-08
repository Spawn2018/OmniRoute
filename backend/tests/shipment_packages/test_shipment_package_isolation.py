from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.location import Location
from app.models.shipment_package import ShipmentPackage
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
        stop_kind="loading",
        sequence_no=1,
        time_zone="Europe/Warsaw",
        status="pending",
        source_ref="fixture://stop/pkg",
        created_by=created_by,
    )


def _parcel(*, organization_id, created_by, shipment_id, stop_id, code: str) -> ShipmentPackage:
    return ShipmentPackage(
        id=uuid4(),
        organization_id=organization_id,
        shipment_id=shipment_id,
        stop_id=stop_id,
        package_code=code,
        package_status="at_stop",
        scan_token=f"omni://shipment-package/{code}",
        source_ref="fixture://shipment-package/iso",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_package_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="pa")
    loc_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-PA", name="PA")
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
    row_a = _parcel(
        organization_id=org_a.id,
        created_by=user_a.id,
        shipment_id=ship_a.id,
        stop_id=halt_a.id,
        code="box_a",
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="pb")
    loc_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="PL-PB", name="PB")
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
    row_b = _parcel(
        organization_id=org_b.id,
        created_by=user_b.id,
        shipment_id=ship_b.id,
        stop_id=halt_b.id,
        code="box_b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(ShipmentPackage))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert (
        await session.scalar(select(ShipmentPackage).where(ShipmentPackage.id == row_b.id)) is None
    )

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(ShipmentPackage))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_package_rejects_foreign_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="px")
    loc_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="PL-PX", name="PX")
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
        _parcel(
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
async def test_shipment_package_rejects_stop_off_route(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]

    await bind_tenant(session, org_a.id)
    ship_one = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="p1")
    ship_two = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="p2")
    loc = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-P2", name="P2")
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
        _parcel(
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
async def test_shipment_package_list_uses_org_shipment_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM shipment_package "
            "WHERE organization_id = :org_id AND shipment_id = :ship_id"
        ),
        {"org_id": org_a.id, "ship_id": uuid4()},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "ix_shipment_package_org_shipment" in joined
