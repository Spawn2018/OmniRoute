from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.charge_code import normalize_charge_code
from app.domain.errors import (
    InvalidPartyData,
    ResourceNotFound,
    UnknownEmailDomain,
    UnknownParty,
    UnknownPartyScorecard,
)
from app.domain.money import Money
from app.domain.party import (
    email_domain_from_address,
    lookup_source_ref,
    manual_source_ref,
    normalize_country_code,
    normalize_credit_pair,
    normalize_email_domain,
    normalize_legal_name,
    normalize_roles,
    normalize_tax_id,
)
from app.domain.party_scorecard import (
    optional_non_negative_hours,
    optional_non_negative_int,
    optional_unit_interval,
    required_sample_size,
    required_window_days,
)
from app.models.carrier_profile import CarrierProfile
from app.models.party import Party
from app.models.party_bank_account import PartyBankAccount
from app.models.party_charge_override import PartyChargeOverride
from app.models.party_contact import PartyContact
from app.models.party_email_domain import PartyEmailDomain
from app.models.party_scorecard import PartyScorecard
from app.repositories.parties.party_repository import PartyRepository
from app.services.parties.lookup import (
    IbanWhitelistDraft,
    PartyDraft,
    lookup_iban_draft,
    lookup_party_draft,
)

_ADAPTERS = frozenset({"none", "maersk", "hapag", "cma", "msc"})
_WHITELIST = frozenset({"pending", "listed", "not_listed", "unavailable"})


def _resolve_tax_token(raw: str) -> str:
    if type(raw) is not str:
        raise UnknownParty("nieznany kontrahent: ")
    stripped = raw.strip()
    if stripped == "":
        raise UnknownParty("nieznany kontrahent: ")
    token = "".join(ch for ch in stripped if not ch.isspace() and ch != "-").upper()
    if token == "":
        raise UnknownParty(f"nieznany kontrahent: {stripped}")
    return token


class PartyService:
    def __init__(self, session: AsyncSession) -> None:
        self._parties = PartyRepository(session)

    async def list_parties(self) -> list[Party]:
        return await self._parties.list_all()

    async def get_party(self, party_id: UUID) -> Party:
        found = await self._parties.get(party_id)
        if found is None:
            raise ResourceNotFound(f"nieznany kontrahent: {party_id}")
        return found

    async def resolve(self, raw: str) -> Party:
        token = _resolve_tax_token(raw)
        found = await self._parties.find_by_tax_id(token)
        if found is None:
            raise UnknownParty(f"nieznany kontrahent: {raw.strip()}")
        return found

    async def resolve_email(self, raw: str) -> Party:
        domain = email_domain_from_address(raw)
        found = await self._parties.find_party_by_email_domain(domain)
        if found is None:
            raise UnknownEmailDomain(f"nieznana domena mailowa: {domain}")
        return found

    async def lookup_party(self, *, tax_id: str, country_code: str) -> PartyDraft:
        token = normalize_tax_id(country_code, tax_id)
        country = normalize_country_code(country_code)
        return lookup_party_draft(tax_id=token, country_code=country)

    async def lookup_iban(self, iban: str) -> IbanWhitelistDraft:
        if type(iban) is not str or iban.strip() == "":
            raise InvalidPartyData("IBAN jest wymagany")
        return lookup_iban_draft(iban)

    async def create_party(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        legal_name: str,
        country_code: str,
        roles: list[str],
        tax_id: str | None = None,
        short_name: str | None = None,
        credit_limit: object | None = None,
        credit_currency: str | None = None,
        source_ref: str | None = None,
        lookup_source: str | None = None,
    ) -> Party:
        country = normalize_country_code(country_code)
        stored_tax: str | None = None
        if tax_id is not None and tax_id.strip() != "":
            stored_tax = normalize_tax_id(country, tax_id)
        limit, currency = normalize_credit_pair(credit_limit, credit_currency)
        origin = (
            lookup_source_ref(lookup_source)
            if lookup_source is not None
            else (source_ref if source_ref is not None else manual_source_ref())
        )
        row = Party(
            id=uuid4(),
            organization_id=organization_id,
            legal_name=normalize_legal_name(legal_name),
            short_name=None if short_name is None else short_name.strip() or None,
            country_code=country,
            tax_id=stored_tax,
            roles=normalize_roles(roles),
            credit_limit=limit,
            credit_currency=currency,
            source_ref=origin,
            is_active=True,
            created_by=user_id,
        )
        try:
            return await self._parties.add(row)
        except IntegrityError as exc:
            raise InvalidPartyData("kontrahent z tym tax_id już istnieje") from exc

    async def list_contacts(self, party_id: UUID) -> list[PartyContact]:
        await self.get_party(party_id)
        return await self._parties.list_contacts(party_id)

    async def create_contact(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        name: str,
        email: str | None = None,
        phone: str | None = None,
        position: str | None = None,
        is_primary: bool = False,
    ) -> PartyContact:
        await self.get_party(party_id)
        label = " ".join(name.split())
        if label == "":
            raise InvalidPartyData("nazwa kontaktu jest wymagana")
        row = PartyContact(
            id=uuid4(),
            organization_id=organization_id,
            party_id=party_id,
            name=label,
            email=None if email is None else email.strip() or None,
            phone=None if phone is None else phone.strip() or None,
            position=None if position is None else position.strip() or None,
            is_primary=is_primary,
            created_by=user_id,
        )
        return await self._parties.add_contact(row)

    async def list_bank_accounts(self, party_id: UUID) -> list[PartyBankAccount]:
        await self.get_party(party_id)
        return await self._parties.list_bank_accounts(party_id)

    async def create_bank_account(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        iban: str,
        currency: str,
        bank_name: str | None = None,
        whitelist_status: str = "pending",
    ) -> PartyBankAccount:
        await self.get_party(party_id)
        token = "".join(iban.split()).upper()
        if token == "":
            raise InvalidPartyData("IBAN jest wymagany")
        status = whitelist_status.strip().lower()
        if status not in _WHITELIST:
            raise InvalidPartyData("whitelist_status spoza słownika")
        money = Money.of(Decimal("0"), currency)
        row = PartyBankAccount(
            id=uuid4(),
            organization_id=organization_id,
            party_id=party_id,
            iban=token,
            currency=money.currency.code,
            bank_name=None if bank_name is None else bank_name.strip() or None,
            whitelist_status=status,
            created_by=user_id,
        )
        return await self._parties.add_bank_account(row)

    async def list_email_domains(self, party_id: UUID) -> list[PartyEmailDomain]:
        await self.get_party(party_id)
        return await self._parties.list_email_domains(party_id)

    async def create_email_domain(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        domain: str,
        source_ref: str | None = None,
    ) -> PartyEmailDomain:
        await self.get_party(party_id)
        row = PartyEmailDomain(
            id=uuid4(),
            organization_id=organization_id,
            party_id=party_id,
            domain=normalize_email_domain(domain),
            source_ref=source_ref if source_ref is not None else manual_source_ref(),
            created_by=user_id,
        )
        try:
            return await self._parties.add_email_domain(row)
        except IntegrityError as exc:
            raise InvalidPartyData("domena już zajęta w tenancie") from exc

    async def list_charge_overrides(self, party_id: UUID) -> list[PartyChargeOverride]:
        await self.get_party(party_id)
        return await self._parties.list_charge_overrides(party_id)

    async def create_charge_override(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        charge_code: str,
        amount: object,
        currency: str,
        lane_pattern: str | None = None,
        basis: str | None = None,
        source_ref: str | None = None,
    ) -> PartyChargeOverride:
        await self.get_party(party_id)
        money = Money.of(amount, currency)
        row = PartyChargeOverride(
            id=uuid4(),
            organization_id=organization_id,
            party_id=party_id,
            charge_code=normalize_charge_code(charge_code),
            amount=money.amount,
            currency=money.currency.code,
            lane_pattern=None if lane_pattern is None else lane_pattern.strip() or None,
            basis=None if basis is None else basis.strip() or None,
            source_ref=source_ref if source_ref is not None else manual_source_ref(),
            created_by=user_id,
        )
        try:
            return await self._parties.add_charge_override(row)
        except IntegrityError as exc:
            raise InvalidPartyData("nieznany kod opłaty albo konflikt wyjątku") from exc

    async def get_carrier_profile(self, party_id: UUID) -> CarrierProfile | None:
        await self.get_party(party_id)
        return await self._parties.get_carrier_profile(party_id)

    async def upsert_carrier_profile(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        scac_code: str | None = None,
        is_nvocc: bool = False,
        rate_source_email: str | None = None,
        api_adapter: str = "none",
        dcsa_tnt_version: str | None = None,
    ) -> CarrierProfile:
        await self.get_party(party_id)
        adapter = api_adapter.strip().lower()
        if adapter not in _ADAPTERS:
            raise InvalidPartyData("api_adapter spoza słownika")
        existing = await self._parties.get_carrier_profile(party_id)
        if existing is not None:
            existing.scac_code = None if scac_code is None else scac_code.strip().upper() or None
            existing.is_nvocc = is_nvocc
            existing.rate_source_email = (
                None if rate_source_email is None else rate_source_email.strip() or None
            )
            existing.api_adapter = adapter
            existing.dcsa_tnt_version = (
                None if dcsa_tnt_version is None else dcsa_tnt_version.strip() or None
            )
            return existing
        row = CarrierProfile(
            id=uuid4(),
            organization_id=organization_id,
            party_id=party_id,
            scac_code=None if scac_code is None else scac_code.strip().upper() or None,
            is_nvocc=is_nvocc,
            rate_source_email=(
                None if rate_source_email is None else rate_source_email.strip() or None
            ),
            api_adapter=adapter,
            dcsa_tnt_version=(
                None if dcsa_tnt_version is None else dcsa_tnt_version.strip() or None
            ),
            created_by=user_id,
        )
        return await self._parties.add_carrier_profile(row)

    async def list_scorecards(self) -> list[PartyScorecard]:
        return await self._parties.list_scorecards()

    async def get_scorecard(self, party_id: UUID) -> PartyScorecard:
        await self.get_party(party_id)
        found = await self._parties.get_scorecard(party_id)
        if found is None:
            raise UnknownPartyScorecard(f"brak karty wyników: {party_id}")
        return found

    async def upsert_scorecard(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        response_rate: object | None = None,
        median_response_hours: object | None = None,
        price_position: object | None = None,
        quote_invoice_match_rate: object | None = None,
        rollover_count: object | None = None,
        sample_size: object | None = None,
        window_days: object | None = None,
    ) -> PartyScorecard:
        await self.get_party(party_id)
        now = datetime.now(UTC)
        stored_response = optional_unit_interval(response_rate, "response_rate")
        stored_hours = optional_non_negative_hours(median_response_hours)
        stored_price = optional_unit_interval(price_position, "price_position")
        stored_match = optional_unit_interval(
            quote_invoice_match_rate,
            "quote_invoice_match_rate",
        )
        stored_rollover = optional_non_negative_int(rollover_count, "rollover_count")
        stored_sample = required_sample_size(sample_size)
        stored_window = required_window_days(window_days)
        origin = manual_source_ref()
        existing = await self._parties.get_scorecard(party_id)
        if existing is not None:
            existing.response_rate = stored_response
            existing.median_response_hours = stored_hours
            existing.price_position = stored_price
            existing.quote_invoice_match_rate = stored_match
            existing.rollover_count = stored_rollover
            existing.sample_size = stored_sample
            existing.window_days = stored_window
            existing.computed_at = now
            existing.source_ref = origin
            return existing
        row = PartyScorecard(
            id=uuid4(),
            organization_id=organization_id,
            party_id=party_id,
            window_days=stored_window,
            sample_size=stored_sample,
            response_rate=stored_response,
            median_response_hours=stored_hours,
            price_position=stored_price,
            quote_invoice_match_rate=stored_match,
            rollover_count=stored_rollover,
            computed_at=now,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._parties.add_scorecard(row)
