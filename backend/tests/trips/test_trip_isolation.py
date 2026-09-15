from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.party import Party
from app.models.resource import Resource
from app.models.trip import Trip


def _fleet(*, organization_id, created_by, kind: str, label: str) -> Resource:
    return Resource(
        id=uuid4(),
        organization_id=organization_id,
        resource_kind=kind,
        display_name=label,
        registration_no=None,
        source_ref="fixture://resource/iso",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_trip_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = Trip(
        id=uuid4(),
        organization_id=org_a.id,
        trip_no="TR-A",
        status="draft",
        source_ref="fixture://trip/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = Trip(
        id=uuid4(),
        organization_id=org_b.id,
        trip_no="TR-B",
        status="planned",
        source_ref="fixture://trip/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(Trip))).all())
    assert {row.trip_no for row in visible_a} == {"TR-A"}
    assert await session.scalar(select(Trip).where(Trip.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(Trip))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_trip_rejects_foreign_resource(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    fleet_b = _fleet(
        organization_id=org_b.id,
        created_by=user_b.id,
        kind="vehicle",
        label="MAN-B",
    )
    session.add(fleet_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    session.add(
        Trip(
            id=uuid4(),
            organization_id=org_a.id,
            trip_no="TR-X",
            status="draft",
            vehicle_id=fleet_b.id,
            source_ref="fixture://trip/x",
            created_by=user_a.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_trip_driver2_fk_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    first = _fleet(
        organization_id=org_a.id,
        created_by=user_a.id,
        kind="driver",
        label="Kowalski",
    )
    second = _fleet(
        organization_id=org_a.id,
        created_by=user_a.id,
        kind="driver",
        label="Nowak",
    )
    session.add_all([first, second])
    await session.flush()
    row = Trip(
        id=uuid4(),
        organization_id=org_a.id,
        trip_no="TR-D2",
        status="draft",
        driver_id=first.id,
        driver2_id=second.id,
        source_ref="fixture://trip/d2",
        created_by=user_a.id,
    )
    session.add(row)
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = await session.scalar(select(Trip).where(Trip.id == row.id))
    assert loaded is not None
    assert loaded.driver_id == first.id
    assert loaded.driver2_id == second.id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_trip_rejects_foreign_driver2(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    fleet_b = _fleet(
        organization_id=org_b.id,
        created_by=user_b.id,
        kind="driver",
        label="Obcy",
    )
    session.add(fleet_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    session.add(
        Trip(
            id=uuid4(),
            organization_id=org_a.id,
            trip_no="TR-Y",
            status="draft",
            driver2_id=fleet_b.id,
            source_ref="fixture://trip/y",
            created_by=user_a.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_trip_rejects_same_uuid_on_both_driver_seats(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    driver = _fleet(
        organization_id=org_a.id,
        created_by=user_a.id,
        kind="driver",
        label="Kowalski",
    )
    session.add(driver)
    await session.flush()
    session.add(
        Trip(
            id=uuid4(),
            organization_id=org_a.id,
            trip_no="TR-Z",
            status="draft",
            driver_id=driver.id,
            driver2_id=driver.id,
            source_ref="fixture://trip/z",
            created_by=user_a.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_trip_list_uses_org_status_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    # Pusta tabela + RLS: EXPLAIN bywa bez nazwy indeksu — katalog jest źródłem prawdy.
    named = await session.execute(
        text(
            "SELECT indexname FROM pg_indexes "
            "WHERE tablename = 'trip' "
            "AND indexname = 'ix_trip_org_status'"
        ),
    )
    assert named.first() is not None
    await session.execute(text("SET LOCAL enable_seqscan = off"))
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM trip "
            "WHERE organization_id = :org_id AND status = 'draft' "
            "AND superseded_by IS NULL"
        ),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_trip_org_status" in joined
        or "Index Scan" in joined
        or "Bitmap Index Scan" in joined
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_trip_route_label_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    row = Trip(
        id=uuid4(),
        organization_id=org_a.id,
        trip_no="TR-L",
        status="draft",
        source_ref="fixture://trip/l",
        route_label="GDYNIA (PL) - BLONIE (PL)",
        created_by=user_a.id,
    )
    session.add(row)
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = await session.scalar(select(Trip).where(Trip.id == row.id))
    assert loaded is not None
    assert loaded.route_label == "GDYNIA (PL) - BLONIE (PL)"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_trip_planned_distance_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    row = Trip(
        id=uuid4(),
        organization_id=org_a.id,
        trip_no="TR-K",
        status="draft",
        source_ref="fixture://trip/k",
        planned_distance_km=Decimal("12.5000"),
        created_by=user_a.id,
    )
    session.add(row)
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = await session.scalar(select(Trip).where(Trip.id == row.id))
    assert loaded is not None
    assert loaded.planned_distance_km == Decimal("12.5000")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_trip_actual_distance_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    row = Trip(
        id=uuid4(),
        organization_id=org_a.id,
        trip_no="TR-L",
        status="draft",
        source_ref="fixture://trip/l",
        actual_distance_km=Decimal("8.2500"),
        created_by=user_a.id,
    )
    session.add(row)
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = await session.scalar(select(Trip).where(Trip.id == row.id))
    assert loaded is not None
    assert loaded.actual_distance_km == Decimal("8.2500")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_trip_subcontractor_party_same_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    vendor = Party(
        id=uuid4(),
        organization_id=org_a.id,
        legal_name="Haul A",
        country_code="PL",
        roles=["subcontractor"],
        source_ref="tenant:manual",
        is_active=True,
        created_by=user_a.id,
    )
    session.add(vendor)
    await session.flush()
    row = Trip(
        id=uuid4(),
        organization_id=org_a.id,
        trip_no="TR-M",
        status="draft",
        source_ref="fixture://trip/m",
        subcontractor_party_id=vendor.id,
        created_by=user_a.id,
    )
    session.add(row)
    await session.flush()
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    loaded = await session.scalar(select(Trip).where(Trip.id == row.id))
    assert loaded is not None
    assert loaded.subcontractor_party_id == vendor.id
