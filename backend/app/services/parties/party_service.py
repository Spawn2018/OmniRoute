from datetime import UTC, datetime
from decimal import Decimal
from typing import NamedTuple
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.charge_code import normalize_charge_code
from app.domain.credit_review import (
    normalize_bureau_attachment_ref,
    normalize_review_date,
    normalize_review_decision,
    normalize_review_note,
)
from app.domain.customer_sop import (
    normalize_sop_blocks_auto,
    normalize_sop_body,
    normalize_sop_code,
    normalize_sop_title,
)
from app.domain.errors import (
    CreditReviewConflict,
    CustomerSopAlreadyApproved,
    CustomerSopConflict,
    InvalidPartyData,
    ResourceNotFound,
    UnknownCreditReview,
    UnknownCustomerSop,
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
    normalize_sanctions_list_ref,
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
from app.models.credit_review import CreditReview
from app.models.customer_sop import CustomerSop
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


def _blank_to_none(raw: str | None, *, upper: bool = False) -> str | None:
    if raw is None:
        return None
    text = raw.strip()
    if text == "":
        return None
    return text.upper() if upper else text


def _party_source_ref(lookup_source: str | None, source_ref: str | None) -> str:
    if lookup_source is not None:
        return lookup_source_ref(lookup_source)
    if source_ref is not None:
        return source_ref
    return manual_source_ref()


def _new_party(
    *,
    organization_id: UUID,
    user_id: UUID,
    legal_name: str,
    country_code: str,
    roles: list[str],
    stored_tax: str | None,
    short_name: str | None,
    credit_limit: Decimal | None,
    credit_currency: str | None,
    origin: str,
) -> Party:
    return Party(
        id=uuid4(),
        organization_id=organization_id,
        legal_name=normalize_legal_name(legal_name),
        short_name=_blank_to_none(short_name),
        country_code=country_code,
        tax_id=stored_tax,
        roles=normalize_roles(roles),
        credit_limit=credit_limit,
        credit_currency=credit_currency,
        source_ref=origin,
        is_active=True,
        created_by=user_id,
    )


class _ScorecardStored(NamedTuple):
    response_rate: Decimal | None
    median_response_hours: Decimal | None
    price_position: Decimal | None
    quote_invoice_match_rate: Decimal | None
    rollover_count: int | None
    sample_size: int
    window_days: int


def _scorecard_stored(
    response_rate: object | None,
    median_response_hours: object | None,
    price_position: object | None,
    quote_invoice_match_rate: object | None,
    rollover_count: object | None,
    sample_size: object | None,
    window_days: object | None,
) -> _ScorecardStored:
    return _ScorecardStored(
        response_rate=optional_unit_interval(response_rate, "response_rate"),
        median_response_hours=optional_non_negative_hours(median_response_hours),
        price_position=optional_unit_interval(price_position, "price_position"),
        quote_invoice_match_rate=optional_unit_interval(
            quote_invoice_match_rate,
            "quote_invoice_match_rate",
        ),
        rollover_count=optional_non_negative_int(rollover_count, "rollover_count"),
        sample_size=required_sample_size(sample_size),
        window_days=required_window_days(window_days),
    )


def _fill_scorecard(
    row: PartyScorecard,
    stored: _ScorecardStored,
    *,
    now: datetime,
    origin: str,
) -> None:
    row.response_rate = stored.response_rate
    row.median_response_hours = stored.median_response_hours
    row.price_position = stored.price_position
    row.quote_invoice_match_rate = stored.quote_invoice_match_rate
    row.rollover_count = stored.rollover_count
    row.sample_size = stored.sample_size
    row.window_days = stored.window_days
    row.computed_at = now
    row.source_ref = origin


def _new_scorecard(
    *,
    organization_id: UUID,
    user_id: UUID,
    party_id: UUID,
    stored: _ScorecardStored,
    now: datetime,
    origin: str,
) -> PartyScorecard:
    return PartyScorecard(
        id=uuid4(),
        organization_id=organization_id,
        party_id=party_id,
        window_days=stored.window_days,
        sample_size=stored.sample_size,
        response_rate=stored.response_rate,
        median_response_hours=stored.median_response_hours,
        price_position=stored.price_position,
        quote_invoice_match_rate=stored.quote_invoice_match_rate,
        rollover_count=stored.rollover_count,
        computed_at=now,
        source_ref=origin,
        created_by=user_id,
    )


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

    async def screen_sanctions(
        self,
        party_id: UUID,
        sanctions_list_ref: object,
    ) -> Party:
        row = await self.get_party(party_id)
        row.sanctions_list_ref = normalize_sanctions_list_ref(sanctions_list_ref)
        row.sanctions_checked_at = datetime.now(UTC)
        return row

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
        origin = _party_source_ref(lookup_source, source_ref)
        try:
            return await self._parties.add(
                _new_party(
                    organization_id=organization_id,
                    user_id=user_id,
                    legal_name=legal_name,
                    country_code=country,
                    roles=roles,
                    stored_tax=stored_tax,
                    short_name=short_name,
                    credit_limit=limit,
                    credit_currency=currency,
                    origin=origin,
                )
            )
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
            email=_blank_to_none(email),
            phone=_blank_to_none(phone),
            position=_blank_to_none(position),
            is_primary=is_primary,
            created_by=user_id,
        )
        return await self._parties.add_contact(row)

    async def get_bank_account(self, account_id: UUID) -> PartyBankAccount:
        found = await self._parties.get_bank_account(account_id)
        if found is None:
            raise ResourceNotFound("nieznany rachunek")
        return found

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
            bank_name=_blank_to_none(bank_name),
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
            lane_pattern=_blank_to_none(lane_pattern),
            basis=_blank_to_none(basis),
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
        scac = _blank_to_none(scac_code, upper=True)
        email = _blank_to_none(rate_source_email)
        dcsa = _blank_to_none(dcsa_tnt_version)
        existing = await self._parties.get_carrier_profile(party_id)
        if existing is not None:
            existing.scac_code = scac
            existing.is_nvocc = is_nvocc
            existing.rate_source_email = email
            existing.api_adapter = adapter
            existing.dcsa_tnt_version = dcsa
            return existing
        row = CarrierProfile(
            id=uuid4(),
            organization_id=organization_id,
            party_id=party_id,
            scac_code=scac,
            is_nvocc=is_nvocc,
            rate_source_email=email,
            api_adapter=adapter,
            dcsa_tnt_version=dcsa,
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
        stored = _scorecard_stored(
            response_rate,
            median_response_hours,
            price_position,
            quote_invoice_match_rate,
            rollover_count,
            sample_size,
            window_days,
        )
        origin = manual_source_ref()
        existing = await self._parties.get_scorecard(party_id)
        if existing is not None:
            _fill_scorecard(existing, stored, now=now, origin=origin)
            return existing
        return await self._parties.add_scorecard(
            _new_scorecard(
                organization_id=organization_id,
                user_id=user_id,
                party_id=party_id,
                stored=stored,
                now=now,
                origin=origin,
            )
        )

    async def list_sops(self) -> list[CustomerSop]:
        return await self._parties.list_sops()

    async def get_sop(self, sop_id: UUID) -> CustomerSop:
        found = await self._parties.get_sop(sop_id)
        if found is None:
            raise ResourceNotFound("nieznana procedura")
        return found

    async def resolve_sop(self, party_id: UUID, code: object) -> CustomerSop:
        token = normalize_sop_code(code)
        await self._require_known_party(party_id)
        found = await self._parties.find_sop_by_party_and_code(party_id, token)
        if found is None:
            raise UnknownCustomerSop(f"nieznana procedura: {token}")
        return found

    async def create_sop(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        code: object,
        title: object,
        body: object,
        blocks_auto: object = True,
    ) -> CustomerSop:
        token = normalize_sop_code(code)
        heading = normalize_sop_title(title)
        text_body = normalize_sop_body(body)
        auto_block = normalize_sop_blocks_auto(blocks_auto)
        await self._require_known_party(party_id)
        duplicate = await self._parties.find_sop_by_party_and_code(party_id, token)
        if duplicate is not None:
            raise CustomerSopConflict(f"procedura {token} już istnieje")
        row = CustomerSop(
            id=uuid4(),
            organization_id=organization_id,
            party_id=party_id,
            status="draft",
            code=token,
            title=heading,
            body=text_body,
            approved_at=None,
            blocks_auto=auto_block,
            source_ref=manual_source_ref(),
            created_by=user_id,
        )
        try:
            return await self._parties.add_sop(row)
        except IntegrityError as exc:
            raise CustomerSopConflict(f"procedura {token} już istnieje") from exc

    async def list_reviews(self) -> list[CreditReview]:
        return await self._parties.list_reviews()

    async def get_review(self, review_id: UUID) -> CreditReview:
        found = await self._parties.get_review(review_id)
        if found is None:
            raise UnknownCreditReview(f"nieznana recenzja kredytowa: {review_id}")
        return found

    async def resolve_review(self, *, party_id: UUID, on_date: object) -> CreditReview:
        day = normalize_review_date(on_date)
        await self._require_known_party(party_id)
        found = await self._parties.find_review_as_of(party_id=party_id, on_date=day)
        if found is None:
            raise UnknownCreditReview(f"brak recenzji kredytowej na {day.isoformat()}")
        return found

    async def create_review(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        review_date: object,
        decision: object,
        note: object = None,
    ) -> CreditReview:
        day = normalize_review_date(review_date)
        verdict = normalize_review_decision(decision)
        stored_note = normalize_review_note(note)
        await self._require_known_party(party_id)
        existing = await self._parties.find_review_as_of(party_id=party_id, on_date=day)
        if existing is not None and existing.review_date == day:
            raise CreditReviewConflict(f"recenzja na {day.isoformat()} już istnieje")
        row = CreditReview(
            id=uuid4(),
            organization_id=organization_id,
            decision=verdict,
            review_date=day,
            party_id=party_id,
            note=stored_note,
            source_ref=manual_source_ref(),
            created_by=user_id,
        )
        try:
            return await self._parties.add_review(row)
        except IntegrityError as exc:
            raise CreditReviewConflict(f"recenzja na {day.isoformat()} już istnieje") from exc

    async def attach_bureau(
        self,
        review_id: UUID,
        bureau_attachment_ref: object,
    ) -> CreditReview:
        row = await self.get_review(review_id)
        row.bureau_attachment_ref = normalize_bureau_attachment_ref(
            bureau_attachment_ref,
        )
        return row

    async def party_blocks_auto(self, party_id: UUID) -> bool:
        await self._require_known_party(party_id)
        return await self._parties.approved_sop_blocks_auto(party_id)

    async def approve_sop(self, sop_id: UUID) -> CustomerSop:
        found = await self._parties.get_sop(sop_id)
        if found is None:
            raise UnknownCustomerSop(f"nieznana procedura: {sop_id}")
        if found.status != "draft":
            raise CustomerSopAlreadyApproved("procedura już zatwierdzona")
        found.status = "approved"
        found.approved_at = datetime.now(UTC)
        return found

    async def _require_known_party(self, party_id: UUID) -> None:
        found = await self._parties.get(party_id)
        if found is None:
            raise UnknownParty(f"nieznany kontrahent: {party_id}")
