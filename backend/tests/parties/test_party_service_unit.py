from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.api.parties import ChargeOverrideResponse, PartyResponse
from app.domain.errors import (
    InvalidPartyData,
    PartyConflict,
    ResourceNotFound,
    UnknownEmailDomain,
    UnknownParty,
)
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
    service._parties.find_by_tax_id = AsyncMock(return_value=None)
    service._parties.find_by_vat_eu = AsyncMock(return_value=None)
    service._parties.find_by_eori = AsyncMock(return_value=None)
    service._parties.find_by_duns = AsyncMock(return_value=None)
    service._parties.add_role_assignment = AsyncMock(side_effect=lambda row: row)
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
    assert created.vat_eu is None
    assert created.eori is None
    assert created.duns is None
    assert created.is_sole_trader is False
    service._parties.add_role_assignment.assert_awaited()


@pytest.mark.asyncio
async def test_service_create_jdg_with_credit_is_rejected() -> None:
    service = _service()
    with pytest.raises(InvalidPartyData, match="JDG"):
        await service.create_party(
            organization_id=uuid4(),
            user_id=uuid4(),
            legal_name="ACME",
            country_code="PL",
            roles=["customer"],
            tax_id="1234563218",
            is_sole_trader=True,
            credit_limit="100.0000",
            credit_currency="PLN",
        )


@pytest.mark.asyncio
async def test_service_create_unknown_parent_is_not_found() -> None:
    service = _service()
    service._parties.find_by_tax_id = AsyncMock(return_value=None)
    service._parties.find_by_vat_eu = AsyncMock(return_value=None)
    service._parties.find_by_eori = AsyncMock(return_value=None)
    service._parties.find_by_duns = AsyncMock(return_value=None)
    service._parties.get = AsyncMock(return_value=None)
    with pytest.raises(ResourceNotFound, match="kontrahent"):
        await service.create_party(
            organization_id=uuid4(),
            user_id=uuid4(),
            legal_name="ACME",
            country_code="DE",
            roles=["vendor"],
            eori="DE1234567",
            parent_party_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_service_create_party_rejects_missing_business_id() -> None:
    service = _service()
    with pytest.raises(InvalidPartyData, match="identyfikator biznesowy"):
        await service.create_party(
            organization_id=uuid4(),
            user_id=uuid4(),
            legal_name="ACME",
            country_code="DE",
            roles=["vendor"],
        )


@pytest.mark.asyncio
async def test_service_create_customer_without_tax_id_is_rejected() -> None:
    service = _service()
    with pytest.raises(InvalidPartyData, match="customer"):
        await service.create_party(
            organization_id=uuid4(),
            user_id=uuid4(),
            legal_name="ACME",
            country_code="DE",
            roles=["customer"],
            eori="DE1234567",
        )


@pytest.mark.asyncio
async def test_service_create_party_duplicate_eori_is_conflict() -> None:
    service = _service()
    existing_id = uuid4()
    service._parties.find_by_tax_id = AsyncMock(return_value=None)
    service._parties.find_by_vat_eu = AsyncMock(return_value=None)
    service._parties.find_by_eori = AsyncMock(
        return_value=SimpleNamespace(id=existing_id),
    )
    service._parties.find_by_duns = AsyncMock(return_value=None)
    with pytest.raises(PartyConflict) as caught:
        await service.create_party(
            organization_id=uuid4(),
            user_id=uuid4(),
            legal_name="ACME",
            country_code="DE",
            roles=["vendor"],
            eori="DE1234567",
        )
    assert caught.value.existing_party_id == existing_id


@pytest.mark.asyncio
async def test_service_get_party_missing() -> None:
    service = _service()
    service._parties.get = AsyncMock(return_value=None)
    with pytest.raises(ResourceNotFound):
        await service.get_party(uuid4())


@pytest.mark.asyncio
async def test_screen_sanctions_keeps_source_ref_and_limit() -> None:
    service = _service()
    row = Party(
        id=uuid4(),
        organization_id=uuid4(),
        legal_name="ACME",
        country_code="PL",
        roles=["customer"],
        source_ref="tenant:manual",
        is_active=True,
        credit_limit=Decimal("10.0000"),
        credit_currency="PLN",
    )
    origin = row.source_ref
    service._parties.get = AsyncMock(return_value=row)
    stored = await service.screen_sanctions(row.id, "  fixture://sanctions/eu-1  ")
    assert stored.sanctions_list_ref == "fixture://sanctions/eu-1"
    assert stored.sanctions_checked_at is not None
    assert stored.source_ref == origin
    assert stored.credit_limit == Decimal("10.0000")


@pytest.mark.asyncio
async def test_screen_sanctions_unknown_party() -> None:
    service = _service()
    service._parties.get = AsyncMock(return_value=None)
    with pytest.raises(ResourceNotFound, match="nieznany kontrahent"):
        await service.screen_sanctions(uuid4(), "fixture://sanctions/eu-1")


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


@pytest.mark.asyncio
async def test_service_create_contact_stores_tracking_consent() -> None:
    service = _service()
    service._parties.get = AsyncMock(return_value=MagicMock())
    stored = MagicMock()
    service._parties.add_contact = AsyncMock(return_value=stored)
    await service.create_contact(
        organization_id=uuid4(),
        user_id=uuid4(),
        party_id=uuid4(),
        name="Anna",
        tracking_consent=True,
    )
    row = service._parties.add_contact.await_args.args[0]
    assert row.tracking_consent is True
    assert row.name == "Anna"


@pytest.mark.asyncio
async def test_service_create_contact_defaults_tracking_consent_false() -> None:
    service = _service()
    service._parties.get = AsyncMock(return_value=MagicMock())
    service._parties.add_contact = AsyncMock(side_effect=lambda row: row)
    row = await service.create_contact(
        organization_id=uuid4(),
        user_id=uuid4(),
        party_id=uuid4(),
        name="Bartek",
    )
    assert row.tracking_consent is False


def test_party_response_formats_credit_and_strips_country() -> None:
    row = SimpleNamespace(
        id=uuid4(),
        organization_id=uuid4(),
        legal_name="ACME",
        short_name=None,
        tax_id="1234563218",
        vat_eu=None,
        eori=None,
        duns=None,
        country_code="PL",
        roles=["customer"],
        credit_limit=Decimal("10.0000"),
        credit_currency="PLN",
        is_sole_trader=False,
        parent_party_id=None,
        is_active=True,
        source_ref="tenant:manual",
        sanctions_list_ref=None,
        sanctions_checked_at=None,
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
