from datetime import time
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.groupage_line import GroupageLine
from app.models.location import Location


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


def _line(*, organization_id, created_by, code: str, origin_id, dest_id) -> GroupageLine:
    return GroupageLine(
        id=uuid4(),
        organization_id=organization_id,
        line_code=code,
        origin_location_id=origin_id,
        destination_location_id=dest_id,
        cutoff_local=time(16, 0),
        transit_days=2,
        operating_dows=[1, 2, 3, 4, 5],
        source_ref="fixture://groupage-line/iso",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_groupage_line_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    start_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-A1", name="A1")
    end_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-A2", name="A2")
    session.add_all([start_a, end_a])
    await session.flush()
    row_a = _line(
        organization_id=org_a.id,
        created_by=user_a.id,
        code="line_a",
        origin_id=start_a.id,
        dest_id=end_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    start_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="PL-B1", name="B1")
    end_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="PL-B2", name="B2")
    session.add_all([start_b, end_b])
    await session.flush()
    row_b = _line(
        organization_id=org_b.id,
        created_by=user_b.id,
        code="line_b",
        origin_id=start_b.id,
        dest_id=end_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(GroupageLine))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(GroupageLine).where(GroupageLine.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(GroupageLine))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_groupage_line_rejects_foreign_location(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    loc_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="PL-X", name="X")
    session.add(loc_b)
    await session.flush()
    await bind_tenant(session, org_a.id)
    loc_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-Y", name="Y")
    session.add(loc_a)
    await session.flush()
    session.add(
        _line(
            organization_id=org_a.id,
            created_by=user_a.id,
            code="cross",
            origin_id=loc_a.id,
            dest_id=loc_b.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_groupage_line_list_uses_org_code_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM groupage_line "
            "WHERE organization_id = :org_id AND line_code = 'wa_hub' "
            "AND superseded_by IS NULL"
        ),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "ix_groupage_line_org_code" in joined
