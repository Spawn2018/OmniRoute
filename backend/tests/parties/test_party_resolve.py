from uuid import uuid4

import pytest

from app.core.database import bind_tenant
from tests.parties._load import load_attr


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_maps_tax_id_to_the_party(session, two_tenants) -> None:
    PartyService = load_attr("app.services.parties.party_service", "PartyService")
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    service = PartyService(session)
    created = await service.create_party(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        legal_name="ACME Sp. z o.o.",
        country_code="PL",
        tax_id="1234563218",
        roles=["customer"],
    )
    resolved = await service.resolve("1234563218")
    assert resolved.id == created.id
    assert resolved.tax_id == "1234563218"
    assert resolved.source_ref == "tenant:manual"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_ignores_letter_case_of_the_tax_id(session, two_tenants) -> None:
    PartyService = load_attr("app.services.parties.party_service", "PartyService")
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    service = PartyService(session)
    await service.create_party(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        legal_name="Hapag counterpart",
        country_code="DE",
        tax_id="de123456789",
        roles=["carrier"],
    )
    assert (await service.resolve("DE123456789")).tax_id == "DE123456789"
    assert (await service.resolve(" De123456789 ")).tax_id == "DE123456789"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_rejects_an_unknown_tax_id(session, two_tenants) -> None:
    errors = load_attr("app.domain.errors", "UnknownParty")
    PartyService = load_attr("app.services.parties.party_service", "PartyService")
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    with pytest.raises(errors, match="GHOST"):
        await PartyService(session).resolve("GHOSTTAX")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_never_reaches_into_another_tenant_catalog(session, two_tenants) -> None:
    errors = load_attr("app.domain.errors", "UnknownParty")
    PartyService = load_attr("app.services.parties.party_service", "PartyService")
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    await bind_tenant(session, org_a.id)
    await PartyService(session).create_party(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        legal_name="ACME A",
        country_code="DE",
        tax_id="DE123456789",
        roles=["customer"],
    )
    await bind_tenant(session, org_b.id)
    with pytest.raises(errors, match="DE123456789"):
        await PartyService(session).resolve("DE123456789")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_does_not_match_a_loose_legal_name(session, two_tenants) -> None:
    errors = load_attr("app.domain.errors", "UnknownParty")
    PartyService = load_attr("app.services.parties.party_service", "PartyService")
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    await PartyService(session).create_party(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        legal_name="ACME Sp. z o.o.",
        country_code="PL",
        tax_id="1234563218",
        roles=["customer"],
    )
    with pytest.raises(errors, match="ACME"):
        await PartyService(session).resolve("ACME Sp. z o.o.")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_party_stores_manual_source_ref(session, two_tenants) -> None:
    PartyService = load_attr("app.services.parties.party_service", "PartyService")
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    created = await PartyService(session).create_party(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        legal_name="  ACME  ",
        country_code="pl",
        roles=[" Customer "],
        tax_id="1234563218",
    )
    assert created.legal_name == "ACME"
    assert created.country_code == "PL"
    assert created.roles == ["customer"]
    assert created.source_ref == "tenant:manual"
    assert created.organization_id == org_a.id
    assert created.id != uuid4()
