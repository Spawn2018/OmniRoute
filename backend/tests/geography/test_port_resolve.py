import pytest

from app.core.database import bind_tenant
from app.domain.errors import UnknownPort
from app.services.geography.port_service import PortService
from app.services.geography.unlocode_ingest import ingest_ports
from tests.geography.unlocode_fixture import FIXTURE_SOURCE_REF, sample_records


async def _seed(session, organization_id) -> None:
    await bind_tenant(session, organization_id)
    await ingest_ports(
        session,
        organization_id=organization_id,
        records=sample_records(),
        source_ref=FIXTURE_SOURCE_REF,
    )
    await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_maps_foreign_port_name_to_unlocode(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await _seed(session, org_a.id)

    resolved = await PortService(session).resolve("Gdingen")
    assert resolved.unlocode == "PLGDY"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_ignores_letter_case_of_alias_and_code(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await _seed(session, org_a.id)
    service = PortService(session)

    assert (await service.resolve("gdingen")).unlocode == "PLGDY"
    assert (await service.resolve("plgdy")).unlocode == "PLGDY"
    assert (await service.resolve(" PL GDY ")).unlocode == "PLGDY"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_rejects_token_outside_the_catalog(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await _seed(session, org_a.id)

    with pytest.raises(UnknownPort, match="ZAMOSC"):
        await PortService(session).resolve("Zamosc")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_never_reaches_into_another_tenant_catalog(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    await _seed(session, org_a.id)

    await bind_tenant(session, org_b.id)
    with pytest.raises(UnknownPort, match="GDINGEN"):
        await PortService(session).resolve("Gdingen")
