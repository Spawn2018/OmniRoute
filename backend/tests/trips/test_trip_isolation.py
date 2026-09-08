from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
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
async def test_trip_list_uses_org_status_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM trip "
            "WHERE organization_id = :org_id AND status = 'draft' "
            "AND superseded_by IS NULL"
        ),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "ix_trip_org_status" in joined
