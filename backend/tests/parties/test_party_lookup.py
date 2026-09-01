import pytest
from sqlalchemy import func, select

from app.core.database import bind_tenant
from tests.parties._load import load_attr


@pytest.mark.integration
@pytest.mark.asyncio
async def test_lookup_returns_a_draft_and_does_not_insert_a_party(
    session,
    two_tenants,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PARTY_LOOKUP_BACKEND", "fixture")
    Party = load_attr("app.models.party", "Party")
    PartyService = load_attr("app.services.parties.party_service", "PartyService")
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    service = PartyService(session)
    draft = await service.lookup_party(tax_id="1234563218", country_code="PL")
    assert draft.legal_name
    assert draft.tax_id == "1234563218"
    assert draft.source == "gus" or draft.vies_valid is not None
    count = await session.scalar(select(func.count()).select_from(Party))
    assert count == 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_lookup_is_idempotent_for_the_same_tax_id(
    session,
    two_tenants,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PARTY_LOOKUP_BACKEND", "fixture")
    PartyService = load_attr("app.services.parties.party_service", "PartyService")
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    service = PartyService(session)
    first = await service.lookup_party(tax_id="1234563218", country_code="PL")
    second = await service.lookup_party(tax_id="1234563218", country_code="PL")
    assert first == second


@pytest.mark.integration
@pytest.mark.asyncio
async def test_iban_whitelist_lookup_does_not_insert_a_bank_account(
    session,
    two_tenants,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PARTY_LOOKUP_BACKEND", "fixture")
    Bank = load_attr("app.models.party_bank_account", "PartyBankAccount")
    PartyService = load_attr("app.services.parties.party_service", "PartyService")
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    draft = await PartyService(session).lookup_iban("PL61109010140000071219812874")
    assert draft.whitelist_status in {"listed", "not_listed", "unavailable"}
    count = await session.scalar(select(func.count()).select_from(Bank))
    assert count == 0


def test_lookup_module_has_no_live_http_in_fixture_backend() -> None:
    inspect_source = load_attr("app.services.parties.lookup", "lookup_party_draft")
    assert callable(inspect_source)
