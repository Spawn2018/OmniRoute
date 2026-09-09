from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.location import Location
from app.models.shipment_leg import ShipmentLeg
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


async def _leg(
    session,
    *,
    org,
    user,
    shipment_id,
    origin_id,
    dest_id,
    suffix: str,
) -> ShipmentLeg:
    row = ShipmentLeg(
        id=uuid4(),
        organization_id=org.id,
        shipment_id=shipment_id,
        origin_location_id=origin_id,
        destination_location_id=dest_id,
        leg_kind="road",
        source_ref=f"fixture://shipment-leg/{suffix}",
        created_by=user.id,
    )
    session.add(row)
    await session.flush()
    return row


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_leg_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="la")
    origin_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="A_ORIG", name="A start")
    dest_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="A_DEST", name="A koniec")
    session.add_all([origin_a, dest_a])
    await session.flush()
    row_a = await _leg(
        session,
        org=org_a,
        user=user_a,
        shipment_id=ship_a.id,
        origin_id=origin_a.id,
        dest_id=dest_a.id,
        suffix="a",
    )

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="lb")
    origin_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="B_ORIG", name="B start")
    dest_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="B_DEST", name="B koniec")
    session.add_all([origin_b, dest_b])
    await session.flush()
    row_b = await _leg(
        session,
        org=org_b,
        user=user_b,
        shipment_id=ship_b.id,
        origin_id=origin_b.id,
        dest_id=dest_b.id,
        suffix="b",
    )

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(ShipmentLeg))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(
        select(ShipmentLeg).where(ShipmentLeg.id == row_b.id),
    ) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(ShipmentLeg))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_leg_rejects_foreign_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="lx")

    await bind_tenant(session, org_a.id)
    origin_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="X_ORIG", name="X start")
    dest_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="X_DEST", name="X koniec")
    session.add_all([origin_a, dest_a])
    await session.flush()
    session.add(
        ShipmentLeg(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_b.id,
            origin_location_id=origin_a.id,
            destination_location_id=dest_a.id,
            leg_kind="road",
            source_ref="fixture://shipment-leg/stolen",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_leg_one_road_per_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="lu")
    origin = _zone(organization_id=org_a.id, created_by=user_a.id, code="U_ORIG", name="U start")
    dest = _zone(organization_id=org_a.id, created_by=user_a.id, code="U_DEST", name="U koniec")
    extra = _zone(organization_id=org_a.id, created_by=user_a.id, code="U_ALT", name="U alt")
    session.add_all([origin, dest, extra])
    await session.flush()
    await _leg(
        session,
        org=org_a,
        user=user_a,
        shipment_id=ship.id,
        origin_id=origin.id,
        dest_id=dest.id,
        suffix="first",
    )
    session.add(
        ShipmentLeg(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship.id,
            origin_location_id=origin.id,
            destination_location_id=extra.id,
            leg_kind="road",
            source_ref="fixture://shipment-leg/second",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_shipment_leg_rejects_unknown_kind(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="lk")
    origin = _zone(organization_id=org_a.id, created_by=user_a.id, code="K_ORIG", name="K start")
    dest = _zone(organization_id=org_a.id, created_by=user_a.id, code="K_DEST", name="K koniec")
    session.add_all([origin, dest])
    await session.flush()
    session.add(
        ShipmentLeg(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship.id,
            origin_location_id=origin.id,
            destination_location_id=dest.id,
            leg_kind="air_parcel",
            source_ref="fixture://shipment-leg/kind",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_air_waybill_hides_other_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="ha")
    origin_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="HA_O", name="HA start")
    dest_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="HA_D", name="HA koniec")
    session.add_all([origin_a, dest_a])
    await session.flush()
    session.add(
        ShipmentLeg(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_a.id,
            origin_location_id=origin_a.id,
            destination_location_id=dest_a.id,
            leg_kind="air",
            hawb_no="HAWB-1",
            source_ref="fixture://shipment-leg/ha",
            created_by=user_a.id,
        )
    )
    await session.flush()

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="hb")
    origin_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="HB_O", name="HB start")
    dest_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="HB_D", name="HB koniec")
    session.add_all([origin_b, dest_b])
    await session.flush()
    session.add(
        ShipmentLeg(
            id=uuid4(),
            organization_id=org_b.id,
            shipment_id=ship_b.id,
            origin_location_id=origin_b.id,
            destination_location_id=dest_b.id,
            leg_kind="air",
            hawb_no="HAWB-1",
            source_ref="fixture://shipment-leg/hb",
            created_by=user_b.id,
        )
    )
    await session.flush()
    visible = list((await session.scalars(select(ShipmentLeg))).all())
    assert len(visible) == 1
    assert visible[0].organization_id == org_b.id
    assert visible[0].hawb_no == "HAWB-1"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_air_waybill_duplicate_hawb_is_refused(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="h1")
    ship_b = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="h2")
    origin = _zone(organization_id=org_a.id, created_by=user_a.id, code="HD_O", name="HD start")
    dest = _zone(organization_id=org_a.id, created_by=user_a.id, code="HD_D", name="HD koniec")
    extra = _zone(organization_id=org_a.id, created_by=user_a.id, code="HD_E", name="HD extra")
    session.add_all([origin, dest, extra])
    await session.flush()
    session.add(
        ShipmentLeg(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_a.id,
            origin_location_id=origin.id,
            destination_location_id=dest.id,
            leg_kind="air",
            hawb_no="HAWB-DUP",
            source_ref="fixture://shipment-leg/h1",
            created_by=user_a.id,
        )
    )
    await session.flush()
    session.add(
        ShipmentLeg(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_b.id,
            origin_location_id=origin.id,
            destination_location_id=extra.id,
            leg_kind="air",
            hawb_no="HAWB-DUP",
            source_ref="fixture://shipment-leg/h2",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError, match="uq_shipment_leg_org_hawb"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_road_leg_rejects_hawb(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="hr")
    origin = _zone(organization_id=org_a.id, created_by=user_a.id, code="HR_O", name="HR start")
    dest = _zone(organization_id=org_a.id, created_by=user_a.id, code="HR_D", name="HR koniec")
    session.add_all([origin, dest])
    await session.flush()
    session.add(
        ShipmentLeg(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship.id,
            origin_location_id=origin.id,
            destination_location_id=dest.id,
            leg_kind="road",
            hawb_no="HAWB-1",
            source_ref="fixture://shipment-leg/hr",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError, match="ck_shipment_leg_air_waybill"):
        await session.flush()
