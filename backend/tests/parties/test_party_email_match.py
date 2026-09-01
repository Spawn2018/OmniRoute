import pytest

from app.core.database import bind_tenant
from tests.parties._load import load_attr


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_email_maps_domain_to_the_party(session, two_tenants) -> None:
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
    await service.create_email_domain(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        party_id=created.id,
        domain="Acme.TEST",
    )
    resolved = await service.resolve_email(" Ops@Acme.TEST ")
    assert resolved.id == created.id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_email_rejects_unknown_domain(session, two_tenants) -> None:
    errors = load_attr("app.domain.errors", "UnknownEmailDomain")
    PartyService = load_attr("app.services.parties.party_service", "PartyService")
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    with pytest.raises(errors, match="ghost.test"):
        await PartyService(session).resolve_email("ops@ghost.test")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resolve_email_never_reaches_into_another_tenant_catalog(
    session,
    two_tenants,
) -> None:
    errors = load_attr("app.domain.errors", "UnknownEmailDomain")
    PartyService = load_attr("app.services.parties.party_service", "PartyService")
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    await bind_tenant(session, org_a.id)
    service_a = PartyService(session)
    created = await service_a.create_party(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        legal_name="ACME A",
        country_code="DE",
        tax_id="DE123456789",
        roles=["customer"],
    )
    await service_a.create_email_domain(
        organization_id=org_a.id,
        user_id=two_tenants["user_a"].id,
        party_id=created.id,
        domain="acme.test",
    )
    await bind_tenant(session, org_b.id)
    with pytest.raises(errors, match="acme.test"):
        await PartyService(session).resolve_email("ops@acme.test")
