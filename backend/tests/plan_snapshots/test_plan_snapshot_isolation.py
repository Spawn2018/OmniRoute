from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.party import Party
from app.models.plan_snapshot import PlanSnapshot
from app.models.quotation import Quotation
from app.models.rate_line import RateLine
from app.models.resource import Resource
from app.models.shipment import Shipment
from app.models.trip import Trip


async def _triple(session, *, organization_id, created_by, suffix: str) -> tuple:
    rate = RateLine(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref=f"tariff://snap-{suffix}",
        created_by=created_by,
    )
    party = Party(
        id=uuid4(),
        organization_id=organization_id,
        legal_name=f"Klient {suffix}",
        country_code="PL",
        roles=["customer"],
        source_ref="tenant:manual",
        is_active=True,
        created_by=created_by,
    )
    session.add_all([rate, party])
    await session.flush()
    quote = Quotation(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        rate_line_id=rate.id,
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref=f"tariff://snap-{suffix}",
        created_by=created_by,
    )
    session.add(quote)
    await session.flush()
    shipment = Shipment(
        id=uuid4(),
        organization_id=organization_id,
        quotation_id=quote.id,
        party_id=party.id,
        source_ref=f"fixture://shipment/snap-{suffix}",
        status="draft",
        created_by=created_by,
    )
    trip = Trip(
        id=uuid4(),
        organization_id=organization_id,
        trip_no=f"SNAP-{suffix}",
        status="draft",
        source_ref=f"fixture://trip/snap-{suffix}",
        created_by=created_by,
    )
    resource = Resource(
        id=uuid4(),
        organization_id=organization_id,
        resource_kind="vehicle",
        display_name=f"Pojazd {suffix}",
        registration_no=None,
        source_ref=f"fixture://resource/snap-{suffix}",
        created_by=created_by,
    )
    session.add_all([shipment, trip, resource])
    await session.flush()
    return shipment.id, trip.id, resource.id


def _row(
    *,
    organization_id,
    created_by,
    shipment_id,
    trip_id,
    resource_id,
    snapshot_code: str = "plan_v1",
    source_ref: str = "tenant:manual",
) -> PlanSnapshot:
    return PlanSnapshot(
        id=uuid4(),
        organization_id=organization_id,
        snapshot_code=snapshot_code,
        shipment_id=shipment_id,
        trip_id=trip_id,
        resource_id=resource_id,
        author_label="Anna",
        recorded_at=datetime(2026, 9, 10, 12, 0, tzinfo=UTC),
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_plan_snapshot_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a, trip_a, res_a = await _triple(
        session, organization_id=org_a.id, created_by=user_a.id, suffix="a"
    )
    row_a = _row(
        organization_id=org_a.id,
        created_by=user_a.id,
        shipment_id=ship_a,
        trip_id=trip_a,
        resource_id=res_a,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    ship_b, trip_b, res_b = await _triple(
        session, organization_id=org_b.id, created_by=user_b.id, suffix="b"
    )
    row_b = _row(
        organization_id=org_b.id,
        created_by=user_b.id,
        shipment_id=ship_b,
        trip_id=trip_b,
        resource_id=res_b,
        snapshot_code="plan_b",
        source_ref="fixture://plan-snapshot/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(PlanSnapshot))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(PlanSnapshot).where(PlanSnapshot.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(PlanSnapshot))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_plan_snapshot_rejects_foreign_shipment(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    await bind_tenant(session, org_b.id)
    ship_b, _trip_b, _res_b = await _triple(
        session, organization_id=org_b.id, created_by=user_b.id, suffix="steal"
    )
    await bind_tenant(session, org_a.id)
    _ship_a, trip_a, res_a = await _triple(
        session, organization_id=org_a.id, created_by=user_a.id, suffix="own"
    )
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            shipment_id=ship_b,
            trip_id=trip_a,
            resource_id=res_a,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_plan_snapshot_restricts_parent_delete(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship_id, trip_id, res_id = await _triple(
        session, organization_id=org_a.id, created_by=user_a.id, suffix="hold"
    )
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            shipment_id=ship_id,
            trip_id=trip_id,
            resource_id=res_id,
        )
    )
    await session.flush()
    shipment = await session.get(Shipment, ship_id)
    assert shipment is not None
    await session.delete(shipment)
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_plan_snapshot_rejects_duplicate_source_ref(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship, trip, res = await _triple(
        session, organization_id=org_a.id, created_by=user_a.id, suffix="dup-ref"
    )
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            shipment_id=ship,
            trip_id=trip,
            resource_id=res,
        )
    )
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            shipment_id=ship,
            trip_id=trip,
            resource_id=res,
            snapshot_code="plan_v2",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_plan_snapshot_rejects_duplicate_code(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    ship, trip, res = await _triple(
        session, organization_id=org_a.id, created_by=user_a.id, suffix="dup-code"
    )
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            shipment_id=ship,
            trip_id=trip,
            resource_id=res,
        )
    )
    await session.flush()
    session.add(
        _row(
            organization_id=org_a.id,
            created_by=user_a.id,
            shipment_id=ship,
            trip_id=trip,
            resource_id=res,
            source_ref="fixture://plan-snapshot/dup-code",
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_plan_snapshot_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM plan_snapshot WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_plan_snapshot_organization_id" in joined
        or "uq_plan_snapshot_org_source_ref" in joined
        or "uq_plan_snapshot_org_code" in joined
    )
