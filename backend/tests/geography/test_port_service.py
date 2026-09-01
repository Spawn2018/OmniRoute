from decimal import Decimal

import pytest

from app.core.database import bind_tenant
from app.domain.errors import PortConflict
from app.services.geography.port_service import PortService
from app.services.geography.unlocode_ingest import ingest_ports
from tests.geography.unlocode_fixture import FIXTURE_SOURCE_REF, sample_records


@pytest.mark.integration
@pytest.mark.asyncio
async def test_manually_added_port_is_unofficial_and_sourced_to_the_tenant(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)

    created = await PortService(session).create_manual_port(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        unlocode="PLXYZ",
        name="Nabrzeże testowe",
        country_code="pl",
        lat=Decimal("54.5"),
        lng=Decimal("18.5"),
        is_seaport=True,
        function_flags=["port"],
        aliases=["Testowy"],
    )

    assert created.unlocode == "PLXYZ"
    assert created.country_code == "PL"
    assert created.is_official is False
    assert created.source_ref == "tenant:manual"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_manual_port_cannot_shadow_a_code_already_in_the_catalog(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    await ingest_ports(
        session,
        organization_id=org_a.id,
        records=sample_records(),
        source_ref=FIXTURE_SOURCE_REF,
    )
    await session.flush()

    with pytest.raises(PortConflict, match="PLGDY"):
        await PortService(session).create_manual_port(
            organization_id=org_a.id,
            user_id=two_tenants["user_a"].id,
            unlocode="PLGDY",
            name="Gdynia własna",
            country_code="PL",
            lat=None,
            lng=None,
            is_seaport=True,
            function_flags=["port"],
            aliases=[],
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_ports_narrows_the_catalog_to_the_search_token(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    await ingest_ports(
        session,
        organization_id=org_a.id,
        records=sample_records(),
        source_ref=FIXTURE_SOURCE_REF,
    )
    await session.flush()

    found = await PortService(session).list_ports(search="gdy")
    assert {row.unlocode for row in found} == {"PLGDY"}
