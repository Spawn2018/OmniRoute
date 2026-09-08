from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.groupage_tariff import GroupageTariff
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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_groupage_tariff_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    zone_a = _zone(organization_id=org_a.id, created_by=user_a.id, code="PL-A1", name="A1")
    session.add(zone_a)
    await session.flush()
    row_a = GroupageTariff(
        id=uuid4(),
        organization_id=org_a.id,
        location_id=zone_a.id,
        tariff_code="band_a",
        chargeable_weight=Decimal("100.0000"),
        amount=Decimal("85.0000"),
        currency="EUR",
        source_ref="fixture://groupage-tariff/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    zone_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="PL-B1", name="B1")
    session.add(zone_b)
    await session.flush()
    row_b = GroupageTariff(
        id=uuid4(),
        organization_id=org_b.id,
        location_id=zone_b.id,
        tariff_code="band_b",
        chargeable_weight=Decimal("200.0000"),
        amount=Decimal("120.0000"),
        currency="PLN",
        source_ref="fixture://groupage-tariff/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(GroupageTariff))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(GroupageTariff).where(GroupageTariff.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(GroupageTariff))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_groupage_tariff_rejects_foreign_location(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    zone_b = _zone(organization_id=org_b.id, created_by=user_b.id, code="PL-BX", name="BX")
    session.add(zone_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    session.add(
        GroupageTariff(
            id=uuid4(),
            organization_id=org_a.id,
            location_id=zone_b.id,
            tariff_code="band_stolen",
            chargeable_weight=Decimal("50.0000"),
            amount=Decimal("10.0000"),
            currency="EUR",
            source_ref="fixture://groupage-tariff/stolen",
            created_by=user_a.id,
        )
    )
    with pytest.raises(IntegrityError):
        await session.flush()
