from uuid import uuid4

import pytest

from app.core.database import bind_tenant
from app.domain.errors import (
    InvalidPostalRange,
    NotAPostalZone,
    PostalRangeOverlap,
    UnknownPostalZone,
)
from app.models.location import Location
from app.services.geography.location_service import LocationService


async def _seed_trojmiasto(session, organization_id, user_id):
    await bind_tenant(session, organization_id)
    service = LocationService(session)
    zone = await service.create_zone(
        organization_id=organization_id,
        user_id=user_id,
        code="trojmiasto",
        name="Trójmiasto",
    )
    await service.add_zone_member(
        organization_id=organization_id,
        user_id=user_id,
        zone_id=zone.id,
        country_code="pl",
        postal_from="81-000",
        postal_to="81-999",
    )
    await session.flush()
    return zone


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_maps_a_polish_postal_code_to_the_tenant_zone(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    zone = await _seed_trojmiasto(session, org_a.id, two_tenants["user_a"].id)

    resolved = await LocationService(session).resolve_postal(
        country_code="PL",
        postal_code="81-198",
    )
    assert resolved.id == zone.id
    assert resolved.code == "TROJMIASTO"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_handles_alphanumeric_british_codes(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    service = LocationService(session)
    zone = await service.create_zone(
        organization_id=org_a.id,
        user_id=user_a.id,
        code="LONDON_C",
        name="Londyn centrum",
    )
    await service.add_zone_member(
        organization_id=org_a.id,
        user_id=user_a.id,
        zone_id=zone.id,
        country_code="GB",
        postal_from="SW1A 0AA",
        postal_to="SW1A 9ZZ",
    )
    await session.flush()

    resolved = await service.resolve_postal(country_code="gb", postal_code="SW1A 1AA")
    assert resolved.id == zone.id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_refuses_a_code_longer_than_the_range(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await _seed_trojmiasto(session, org_a.id, two_tenants["user_a"].id)

    # 811989 wpada leksykograficznie w [81000, 81999]; filtr długości to odrzuca.
    with pytest.raises(UnknownPostalZone, match="811989"):
        await LocationService(session).resolve_postal(country_code="PL", postal_code="811989")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_refuses_a_code_outside_every_range(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await _seed_trojmiasto(session, org_a.id, two_tenants["user_a"].id)

    with pytest.raises(UnknownPostalZone, match="00950"):
        await LocationService(session).resolve_postal(country_code="PL", postal_code="00-950")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_never_reaches_into_another_tenant_zones(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    await _seed_trojmiasto(session, org_a.id, two_tenants["user_a"].id)

    await bind_tenant(session, org_b.id)
    with pytest.raises(UnknownPostalZone):
        await LocationService(session).resolve_postal(country_code="PL", postal_code="81-198")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_country_stays_on_the_member_so_a_zone_may_span_countries(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    zone = await _seed_trojmiasto(session, org_a.id, user_a.id)
    service = LocationService(session)
    await service.add_zone_member(
        organization_id=org_a.id,
        user_id=user_a.id,
        zone_id=zone.id,
        country_code="DE",
        postal_from="20000",
        postal_to="20999",
    )
    await session.flush()

    assert (await service.resolve_postal(country_code="PL", postal_code="81198")).id == zone.id
    assert (await service.resolve_postal(country_code="DE", postal_code="20095")).id == zone.id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_overlapping_range_surfaces_as_a_domain_error(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    zone = await _seed_trojmiasto(session, org_a.id, user_a.id)

    with pytest.raises(PostalRangeOverlap):
        await LocationService(session).add_zone_member(
            organization_id=org_a.id,
            user_id=user_a.id,
            zone_id=zone.id,
            country_code="PL",
            postal_from="81-500",
            postal_to="81-600",
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_range_may_not_hang_on_a_location_that_is_not_a_zone(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    address = Location(
        id=uuid4(),
        organization_id=org_a.id,
        kind="address",
        name="Magazyn Kowale",
        country_code="PL",
        city="Kowale",
        address_line="Magnacka 1",
        postal_code="80180",
        source_ref="tenant:manual",
    )
    session.add(address)
    await session.flush()

    with pytest.raises(NotAPostalZone):
        await LocationService(session).add_zone_member(
            organization_id=org_a.id,
            user_id=user_a.id,
            zone_id=address.id,
            country_code="PL",
            postal_from="80-100",
            postal_to="80-199",
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_reversed_range_never_reaches_the_database(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    zone = await _seed_trojmiasto(session, org_a.id, user_a.id)

    with pytest.raises(InvalidPostalRange, match="odwrócony"):
        await LocationService(session).add_zone_member(
            organization_id=org_a.id,
            user_id=user_a.id,
            zone_id=zone.id,
            country_code="PL",
            postal_from="82-999",
            postal_to="82-000",
        )
