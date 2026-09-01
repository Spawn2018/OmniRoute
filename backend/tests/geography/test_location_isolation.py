from uuid import UUID, uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.location import Location, LocationZoneMember
from app.models.port import Port

_MANUAL = "tenant:manual"


def _zone(*, organization_id: UUID, code: str, name: str, created_by: UUID) -> Location:
    return Location(
        id=uuid4(),
        organization_id=organization_id,
        kind="postal_zone",
        name=name,
        code=code,
        source_ref=_MANUAL,
        created_by=created_by,
    )


def _member(
    *,
    organization_id: UUID,
    zone_location_id: UUID,
    postal_from: str,
    postal_to: str,
    country_code: str = "PL",
) -> LocationZoneMember:
    return LocationZoneMember(
        id=uuid4(),
        organization_id=organization_id,
        zone_location_id=zone_location_id,
        country_code=country_code,
        postal_from=postal_from,
        postal_to=postal_to,
        source_ref=_MANUAL,
    )


def _port(*, organization_id: UUID, unlocode: str) -> Port:
    return Port(
        id=uuid4(),
        organization_id=organization_id,
        unlocode=unlocode,
        name=unlocode,
        country_code=unlocode[:2],
        is_seaport=True,
        function_flags=["port"],
        aliases=[],
        is_official=True,
        source_ref="github:cristan/improved-un-locodes@fixture",
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_location_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]

    zone_a = _zone(
        organization_id=org_a.id,
        code="TROJMIASTO",
        name="Trójmiasto",
        created_by=two_tenants["user_a"].id,
    )
    zone_b = _zone(
        organization_id=org_b.id,
        code="HAMBURG",
        name="Hamburg",
        created_by=two_tenants["user_b"].id,
    )

    await bind_tenant(session, org_a.id)
    session.add(zone_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(zone_b)
    await session.flush()

    session.expunge_all()

    await bind_tenant(session, org_a.id)
    assert {row.id for row in (await session.scalars(select(Location))).all()} == {zone_a.id}
    assert await session.scalar(select(Location).where(Location.id == zone_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    assert {row.id for row in (await session.scalars(select(Location))).all()} == {zone_b.id}
    assert await session.scalar(select(Location).where(Location.id == zone_a.id)) is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_zone_member_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]

    zone_a = _zone(
        organization_id=org_a.id,
        code="TROJMIASTO",
        name="Trójmiasto",
        created_by=two_tenants["user_a"].id,
    )
    zone_b = _zone(
        organization_id=org_b.id,
        code="TROJMIASTO",
        name="Trójmiasto",
        created_by=two_tenants["user_b"].id,
    )

    await bind_tenant(session, org_a.id)
    session.add(zone_a)
    member_a = _member(
        organization_id=org_a.id,
        zone_location_id=zone_a.id,
        postal_from="81000",
        postal_to="81999",
    )
    session.add(member_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(zone_b)
    member_b = _member(
        organization_id=org_b.id,
        zone_location_id=zone_b.id,
        postal_from="81000",
        postal_to="81999",
    )
    session.add(member_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible = list((await session.scalars(select(LocationZoneMember))).all())
    assert {row.id for row in visible} == {member_a.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_overlapping_range_inside_one_tenant_is_refused_by_the_database(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]

    await bind_tenant(session, org_a.id)
    zone = _zone(
        organization_id=org_a.id,
        code="TROJMIASTO",
        name="Trójmiasto",
        created_by=two_tenants["user_a"].id,
    )
    session.add(zone)
    session.add(
        _member(
            organization_id=org_a.id,
            zone_location_id=zone.id,
            postal_from="81000",
            postal_to="81999",
        )
    )
    await session.flush()

    session.add(
        _member(
            organization_id=org_a.id,
            zone_location_id=zone.id,
            postal_from="81500",
            postal_to="81600",
        )
    )
    with pytest.raises(IntegrityError, match="ex_zone_member_no_overlap"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_the_same_range_passes_for_the_second_tenant(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]

    await bind_tenant(session, org_a.id)
    zone_a = _zone(
        organization_id=org_a.id,
        code="TROJMIASTO",
        name="Trójmiasto",
        created_by=two_tenants["user_a"].id,
    )
    session.add(zone_a)
    session.add(
        _member(
            organization_id=org_a.id,
            zone_location_id=zone_a.id,
            postal_from="81000",
            postal_to="81999",
        )
    )
    await session.flush()

    await bind_tenant(session, org_b.id)
    zone_b = _zone(
        organization_id=org_b.id,
        code="POMORZE",
        name="Pomorze",
        created_by=two_tenants["user_b"].id,
    )
    session.add(zone_b)
    session.add(
        _member(
            organization_id=org_b.id,
            zone_location_id=zone_b.id,
            postal_from="81000",
            postal_to="81999",
        )
    )
    await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_zone_member_may_not_point_at_another_tenant_zone(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]

    await bind_tenant(session, org_a.id)
    zone_a = _zone(
        organization_id=org_a.id,
        code="TROJMIASTO",
        name="Trójmiasto",
        created_by=two_tenants["user_a"].id,
    )
    session.add(zone_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(
        _member(
            organization_id=org_b.id,
            zone_location_id=zone_a.id,
            postal_from="81000",
            postal_to="81999",
        )
    )
    with pytest.raises(IntegrityError, match="fk_location_zone_member_zone"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_location_may_not_point_at_another_tenant_port(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]

    await bind_tenant(session, org_a.id)
    port_a = _port(organization_id=org_a.id, unlocode="PLGDY")
    session.add(port_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    session.add(
        Location(
            id=uuid4(),
            organization_id=org_b.id,
            kind="unlocode",
            name="Gdynia",
            port_id=port_a.id,
            country_code="PL",
            source_ref=_MANUAL,
        )
    )
    with pytest.raises(IntegrityError, match="fk_location_port"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_zone_without_tenant_context_is_invisible(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]

    await bind_tenant(session, org_a.id)
    session.add(
        _zone(
            organization_id=org_a.id,
            code="TROJMIASTO",
            name="Trójmiasto",
            created_by=two_tenants["user_a"].id,
        )
    )
    await session.flush()
    session.expunge_all()

    await session.execute(text("SELECT set_config('app.current_org', '', true)"))
    assert list((await session.scalars(select(Location))).all()) == []
