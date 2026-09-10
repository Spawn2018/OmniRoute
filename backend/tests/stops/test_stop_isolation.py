from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.location import Location
from app.models.stop import Stop
from tests.sales_invoices.test_sales_invoice_isolation import _booked

_CLOCK = datetime(2026, 9, 9, 12, 0, tzinfo=UTC)


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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stop_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="sa")
    loc_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-A", name="Strefa A")
    session.add(loc_a)
    await session.flush()
    row_a = Stop(
        id=uuid4(),
        organization_id=org_a.id,
        shipment_id=ship_a.id,
        location_id=loc_a.id,
        stop_kind="loading",
        sequence_no=1,
        time_zone="Europe/Warsaw",
        status="pending",
        source_ref="fixture://stop/a",
        eta_physical=_CLOCK,
        eta_legal=_CLOCK,
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="sb")
    loc_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="PL-B", name="Strefa B")
    session.add(loc_b)
    await session.flush()
    row_b = Stop(
        id=uuid4(),
        organization_id=org_b.id,
        shipment_id=ship_b.id,
        location_id=loc_b.id,
        stop_kind="unloading",
        sequence_no=1,
        time_zone="Europe/Berlin",
        status="at_stop",
        source_ref="fixture://stop/b",
        eta_physical=_CLOCK,
        eta_legal=_CLOCK,
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(Stop))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert visible_a[0].eta_physical is not None
    assert visible_a[0].eta_legal is not None
    assert await session.scalar(select(Stop).where(Stop.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(Stop))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stop_rejects_foreign_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="sx")
    await bind_tenant(session, org_a.id)
    loc_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-X", name="Strefa X")
    session.add(loc_a)
    await session.flush()
    session.add(
        Stop(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_b.id,
            location_id=loc_a.id,
            stop_kind="loading",
            sequence_no=1,
            time_zone="Europe/Warsaw",
            status="pending",
            source_ref="fixture://stop/x",
            eta_physical=_CLOCK,
            eta_legal=_CLOCK,
            created_by=user_a.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stop_list_uses_org_shipment_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    await session.execute(text("SET LOCAL enable_seqscan = off"))
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM stop "
            "WHERE organization_id = :org_id AND shipment_id = :ship "
            "AND superseded_by IS NULL"
        ),
        {"org_id": org_a.id, "ship": uuid4()},
    )
    joined = " ".join(str(row[0]) for row in plan)
    catalog = await session.execute(
        text("SELECT indexname FROM pg_indexes WHERE tablename = 'stop'"),
    )
    names = {row[0] for row in catalog}
    assert "ix_stop_org_shipment" in names
    assert "Index Scan" in joined
    assert "organization_id" in joined
    assert "shipment_id" in joined


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stop_rejects_foreign_location(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    loc_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="PL-L", name="Strefa L")
    session.add(loc_b)
    await session.flush()
    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="sl")
    session.add(
        Stop(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_a.id,
            location_id=loc_b.id,
            stop_kind="loading",
            sequence_no=1,
            time_zone="Europe/Warsaw",
            status="pending",
            source_ref="fixture://stop/loc",
            eta_physical=_CLOCK,
            eta_legal=_CLOCK,
            created_by=user_a.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stop_group_code_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="sg")
    loc_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-G", name="Strefa G")
    session.add(loc_a)
    await session.flush()
    first = Stop(
        id=uuid4(),
        organization_id=org_a.id,
        shipment_id=ship_a.id,
        location_id=loc_a.id,
        stop_kind="loading",
        sequence_no=1,
        time_zone="Europe/Warsaw",
        status="pending",
        source_ref="fixture://stop/g1",
        stop_group_code="ZA-WY-1",
        eta_physical=_CLOCK,
        eta_legal=_CLOCK,
        created_by=user_a.id,
    )
    second = Stop(
        id=uuid4(),
        organization_id=org_a.id,
        shipment_id=ship_a.id,
        location_id=loc_a.id,
        stop_kind="unloading",
        sequence_no=2,
        time_zone="Europe/Warsaw",
        status="pending",
        source_ref="fixture://stop/g2",
        stop_group_code="ZA-WY-1",
        eta_physical=_CLOCK,
        eta_legal=_CLOCK,
        created_by=user_a.id,
    )
    session.add_all([first, second])
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Stop))).all())
    assert {row.stop_group_code for row in loaded} == {"ZA-WY-1"}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stop_rejects_loose_group_code(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="sbad")
    loc_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-Q", name="Strefa Q")
    session.add(loc_a)
    await session.flush()
    session.add(
        Stop(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_a.id,
            location_id=loc_a.id,
            stop_kind="loading",
            sequence_no=1,
            time_zone="Europe/Warsaw",
            status="pending",
            source_ref="fixture://stop/bad",
            stop_group_code="x",
            eta_physical=_CLOCK,
            eta_legal=_CLOCK,
            created_by=user_a.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stop_notes_for_driver_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="nt")
    loc_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-N", name="Strefa N")
    session.add(loc_a)
    await session.flush()
    session.add(
        Stop(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_a.id,
            location_id=loc_a.id,
            stop_kind="loading",
            sequence_no=1,
            time_zone="Europe/Warsaw",
            status="pending",
            source_ref="fixture://stop/n1",
            notes_for_driver="brama B, dzwonek 2",
            eta_physical=_CLOCK,
            eta_legal=_CLOCK,
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Stop))).all())
    assert loaded[0].notes_for_driver == "brama B, dzwonek 2"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stop_weight_kg_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="wt")
    loc_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-W", name="Strefa W")
    session.add(loc_a)
    await session.flush()
    session.add(
        Stop(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_a.id,
            location_id=loc_a.id,
            stop_kind="loading",
            sequence_no=1,
            time_zone="Europe/Warsaw",
            status="pending",
            source_ref="fixture://stop/w1",
            weight_kg=Decimal("12.5000"),
            eta_physical=_CLOCK,
            eta_legal=_CLOCK,
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Stop))).all())
    assert loaded[0].weight_kg == Decimal("12.5000")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stop_quantity_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="qty")
    loc_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-Q", name="Strefa Q")
    session.add(loc_a)
    await session.flush()
    session.add(
        Stop(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_a.id,
            location_id=loc_a.id,
            stop_kind="loading",
            sequence_no=1,
            time_zone="Europe/Warsaw",
            status="pending",
            source_ref="fixture://stop/q1",
            quantity=12,
            eta_physical=_CLOCK,
            eta_legal=_CLOCK,
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Stop))).all())
    assert loaded[0].quantity == 12


@pytest.mark.integration
@pytest.mark.asyncio
async def test_stop_packaging_code_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="pk")
    loc_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-P", name="Strefa P")
    session.add(loc_a)
    await session.flush()
    session.add(
        Stop(
            id=uuid4(),
            organization_id=org_a.id,
            shipment_id=ship_a.id,
            location_id=loc_a.id,
            stop_kind="loading",
            sequence_no=1,
            time_zone="Europe/Warsaw",
            status="pending",
            source_ref="fixture://stop/p1",
            packaging_code="EUR",
            eta_physical=_CLOCK,
            eta_legal=_CLOCK,
            created_by=user_a.id,
        ),
    )
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = list((await session.scalars(select(Stop))).all())
    assert loaded[0].packaging_code == "EUR"
