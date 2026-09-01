from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.api.parties import ChargeOverrideResponse, PartyResponse
from app.domain.errors import InvalidPartyData, ResourceNotFound, UnknownEmailDomain, UnknownParty
from app.models.party import Party
from app.services.parties.lookup import lookup_iban_draft, lookup_party_draft
from app.services.parties.party_service import PartyService


def _service() -> PartyService:
    service = PartyService(MagicMock())
    service._parties = MagicMock()
    return service


def test_lookup_unknown_tax_id_still_returns_a_named_draft() -> None:
    draft = lookup_party_draft(tax_id="9999999999", country_code="DE")
    assert draft.legal_name
    assert draft.tax_id == "9999999999"


def test_lookup_iban_fixture_marks_sample_listed() -> None:
    draft = lookup_iban_draft(" PL61109010140000071219812874 ")
    assert draft.whitelist_status == "listed"


def test_lookup_iban_unknown_is_unavailable() -> None:
    assert lookup_iban_draft("DE00").whitelist_status == "unavailable"


@pytest.mark.asyncio
async def test_service_lookup_does_not_touch_repository() -> None:
    service = _service()
    draft = await service.lookup_party(tax_id="1234563218", country_code="pl")
    assert draft.tax_id == "1234563218"
    service._parties.add.assert_not_called()


@pytest.mark.asyncio
async def test_service_resolve_unknown_tax_id() -> None:
    service = _service()
    service._parties.find_by_tax_id = AsyncMock(return_value=None)
    with pytest.raises(UnknownParty, match="GHOST"):
        await service.resolve("GHOSTTAX")


@pytest.mark.asyncio
async def test_service_resolve_email_unknown_domain() -> None:
    service = _service()
    service._parties.find_party_by_email_domain = AsyncMock(return_value=None)
    with pytest.raises(UnknownEmailDomain, match="ghost.test"):
        await service.resolve_email("ops@ghost.test")


@pytest.mark.asyncio
async def test_service_resolve_email_rejects_address_without_at() -> None:
    service = _service()
    with pytest.raises(InvalidPartyData, match="@"):
        await service.resolve_email("ghost.test")


@pytest.mark.asyncio
async def test_service_create_party_normalizes_and_adds() -> None:
    service = _service()

    async def add(row: Party) -> Party:
        return row

    service._parties.add = add
    created = await service.create_party(
        organization_id=uuid4(),
        user_id=uuid4(),
        legal_name="  ACME  ",
        country_code="pl",
        roles=[" Customer "],
        tax_id="1234563218",
    )
    assert created.legal_name == "ACME"
    assert created.country_code == "PL"
    assert created.roles == ["customer"]
    assert created.source_ref == "tenant:manual"
    assert created.tax_id == "1234563218"


@pytest.mark.asyncio
async def test_service_get_party_missing() -> None:
    service = _service()
    service._parties.get = AsyncMock(return_value=None)
    with pytest.raises(ResourceNotFound):
        await service.get_party(uuid4())


@pytest.mark.asyncio
async def test_service_create_contact_rejects_blank_name() -> None:
    service = _service()
    service._parties.get = AsyncMock(return_value=MagicMock())
    with pytest.raises(InvalidPartyData, match="kontaktu"):
        await service.create_contact(
            organization_id=uuid4(),
            user_id=uuid4(),
            party_id=uuid4(),
            name="  ",
        )


def test_party_response_formats_credit_and_strips_country() -> None:
    row = SimpleNamespace(
        id=uuid4(),
        organization_id=uuid4(),
        legal_name="ACME",
        short_name=None,
        tax_id="1234563218",
        country_code="PL",
        roles=["customer"],
        credit_limit=Decimal("10.0000"),
        credit_currency="PLN",
        is_active=True,
        source_ref="tenant:manual",
    )
    dto = PartyResponse.from_row(row)  # type: ignore[arg-type]
    assert dto.country_code == "PL"
    assert dto.credit_limit == "10.0000"


def test_charge_override_response_formats_amount() -> None:
    row = SimpleNamespace(
        id=uuid4(),
        party_id=uuid4(),
        charge_code="THC",
        amount=Decimal("15.5000"),
        currency="USD",
        lane_pattern=None,
        basis=None,
        source_ref="tenant:manual",
    )
    dto = ChargeOverrideResponse.from_row(row)  # type: ignore[arg-type]
    assert dto.amount == "15.5000"
