from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.carrier_profile import CarrierProfile
from app.models.party import Party
from app.models.party_bank_account import PartyBankAccount
from app.models.party_charge_override import PartyChargeOverride
from app.models.party_contact import PartyContact
from app.models.party_email_domain import PartyEmailDomain
from app.services.parties.lookup import IbanWhitelistDraft, PartyDraft
from app.services.parties.party_service import PartyService

router = APIRouter(prefix="/parties", tags=["parties"])

_PARTIES = require_permission("can_manage_parties", "organization")


class PartyCreate(BaseModel):
    legal_name: str = Field(min_length=1, max_length=256)
    country_code: str = Field(min_length=2, max_length=2)
    roles: list[str] = Field(min_length=1)
    tax_id: str | None = Field(default=None, max_length=32)
    short_name: str | None = Field(default=None, max_length=64)
    credit_limit: str | None = None
    credit_currency: str | None = Field(default=None, min_length=3, max_length=3)
    lookup_source: str | None = None


class PartyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    legal_name: str
    short_name: str | None
    tax_id: str | None
    country_code: str
    roles: list[str]
    credit_limit: str | None
    credit_currency: str | None
    is_active: bool
    source_ref: str
    sanctions_list_ref: str | None
    sanctions_checked_at: datetime | None

    @classmethod
    def from_row(cls, row: Party) -> "PartyResponse":
        limit = None if row.credit_limit is None else format(row.credit_limit, "f")
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            legal_name=row.legal_name,
            short_name=row.short_name,
            tax_id=row.tax_id,
            country_code=row.country_code.strip(),
            roles=list(row.roles),
            credit_limit=limit,
            credit_currency=row.credit_currency,
            is_active=row.is_active,
            source_ref=row.source_ref,
            sanctions_list_ref=row.sanctions_list_ref,
            sanctions_checked_at=row.sanctions_checked_at,
        )


class PartyLookupRequest(BaseModel):
    tax_id: str = Field(min_length=1, max_length=32)
    country_code: str = Field(min_length=2, max_length=2)


class PartyDraftResponse(BaseModel):
    legal_name: str
    tax_id: str
    source: str
    vies_valid: bool | None

    @classmethod
    def from_draft(cls, draft: PartyDraft) -> "PartyDraftResponse":
        return cls(
            legal_name=draft.legal_name,
            tax_id=draft.tax_id,
            source=draft.source,
            vies_valid=draft.vies_valid,
        )


class IbanLookupRequest(BaseModel):
    iban: str = Field(min_length=1, max_length=34)


class IbanDraftResponse(BaseModel):
    iban: str
    whitelist_status: str

    @classmethod
    def from_draft(cls, draft: IbanWhitelistDraft) -> "IbanDraftResponse":
        return cls(iban=draft.iban, whitelist_status=draft.whitelist_status)


class ContactCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    email: str | None = None
    phone: str | None = None
    position: str | None = None
    is_primary: bool = False


class ContactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    party_id: UUID
    name: str
    email: str | None
    phone: str | None
    position: str | None
    is_primary: bool

    @classmethod
    def from_row(cls, row: PartyContact) -> "ContactResponse":
        return cls.model_validate(row)


class BankAccountCreate(BaseModel):
    iban: str = Field(min_length=1, max_length=34)
    currency: str = Field(min_length=3, max_length=3)
    bank_name: str | None = None
    whitelist_status: str = "pending"


class BankAccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    party_id: UUID
    iban: str
    currency: str
    bank_name: str | None
    whitelist_status: str

    @classmethod
    def from_row(cls, row: PartyBankAccount) -> "BankAccountResponse":
        return cls.model_validate(row)


class EmailDomainCreate(BaseModel):
    domain: str = Field(min_length=1, max_length=256)
    source_ref: str | None = None


class EmailDomainResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    party_id: UUID
    domain: str
    source_ref: str

    @classmethod
    def from_row(cls, row: PartyEmailDomain) -> "EmailDomainResponse":
        return cls.model_validate(row)


class ChargeOverrideCreate(BaseModel):
    charge_code: str = Field(min_length=2, max_length=32)
    amount: str = Field(min_length=1, max_length=32)
    currency: str = Field(min_length=3, max_length=3)
    lane_pattern: str | None = None
    basis: str | None = None
    source_ref: str | None = None


class ChargeOverrideResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    party_id: UUID
    charge_code: str
    amount: str
    currency: str
    lane_pattern: str | None
    basis: str | None
    source_ref: str

    @classmethod
    def from_row(cls, row: PartyChargeOverride) -> "ChargeOverrideResponse":
        return cls(
            id=row.id,
            party_id=row.party_id,
            charge_code=row.charge_code,
            amount=format(row.amount, "f"),
            currency=row.currency,
            lane_pattern=row.lane_pattern,
            basis=row.basis,
            source_ref=row.source_ref,
        )


class CarrierProfileUpsert(BaseModel):
    scac_code: str | None = None
    is_nvocc: bool = False
    rate_source_email: str | None = None
    api_adapter: str = "none"
    dcsa_tnt_version: str | None = None


class CarrierProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    party_id: UUID
    scac_code: str | None
    is_nvocc: bool
    rate_source_email: str | None
    api_adapter: str
    dcsa_tnt_version: str | None

    @classmethod
    def from_row(cls, row: CarrierProfile) -> "CarrierProfileResponse":
        return cls.model_validate(row)


@router.get("", response_model=list[PartyResponse])
async def list_parties(
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PartyResponse]:
    rows = await PartyService(session).list_parties()
    return [PartyResponse.from_row(row) for row in rows]


@router.get("/resolve", response_model=PartyResponse)
async def resolve_party(
    tax_id: str = Query(..., min_length=1, max_length=64),
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> PartyResponse:
    row = await PartyService(session).resolve(tax_id)
    return PartyResponse.from_row(row)


@router.get("/resolve-email", response_model=PartyResponse)
async def resolve_party_email(
    email: str = Query(..., min_length=3, max_length=256),
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> PartyResponse:
    row = await PartyService(session).resolve_email(email)
    return PartyResponse.from_row(row)


@router.post("/lookup", response_model=PartyDraftResponse)
async def lookup_party(
    body: PartyLookupRequest,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> PartyDraftResponse:
    draft = await PartyService(session).lookup_party(
        tax_id=body.tax_id,
        country_code=body.country_code,
    )
    return PartyDraftResponse.from_draft(draft)


@router.post("/iban-lookup", response_model=IbanDraftResponse)
async def lookup_iban(
    body: IbanLookupRequest,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> IbanDraftResponse:
    draft = await PartyService(session).lookup_iban(body.iban)
    return IbanDraftResponse.from_draft(draft)


@router.post("", response_model=PartyResponse, status_code=status.HTTP_201_CREATED)
async def create_party(
    body: PartyCreate,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PartyResponse:
    row = await PartyService(session).create_party(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        legal_name=body.legal_name,
        country_code=body.country_code,
        roles=body.roles,
        tax_id=body.tax_id,
        short_name=body.short_name,
        credit_limit=body.credit_limit,
        credit_currency=body.credit_currency,
        lookup_source=body.lookup_source,
    )
    await session.commit()
    return PartyResponse.from_row(row)


@router.get("/{party_id}/contacts", response_model=list[ContactResponse])
async def list_contacts(
    party_id: UUID,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ContactResponse]:
    rows = await PartyService(session).list_contacts(party_id)
    return [ContactResponse.from_row(row) for row in rows]


@router.post(
    "/{party_id}/contacts",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(
    party_id: UUID,
    body: ContactCreate,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ContactResponse:
    row = await PartyService(session).create_contact(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=party_id,
        name=body.name,
        email=body.email,
        phone=body.phone,
        position=body.position,
        is_primary=body.is_primary,
    )
    await session.commit()
    return ContactResponse.from_row(row)


@router.get("/{party_id}/bank-accounts", response_model=list[BankAccountResponse])
async def list_bank_accounts(
    party_id: UUID,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[BankAccountResponse]:
    rows = await PartyService(session).list_bank_accounts(party_id)
    return [BankAccountResponse.from_row(row) for row in rows]


@router.post(
    "/{party_id}/bank-accounts",
    response_model=BankAccountResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_bank_account(
    party_id: UUID,
    body: BankAccountCreate,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> BankAccountResponse:
    row = await PartyService(session).create_bank_account(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=party_id,
        iban=body.iban,
        currency=body.currency,
        bank_name=body.bank_name,
        whitelist_status=body.whitelist_status,
    )
    await session.commit()
    return BankAccountResponse.from_row(row)


@router.get("/{party_id}/email-domains", response_model=list[EmailDomainResponse])
async def list_email_domains(
    party_id: UUID,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[EmailDomainResponse]:
    rows = await PartyService(session).list_email_domains(party_id)
    return [EmailDomainResponse.from_row(row) for row in rows]


@router.post(
    "/{party_id}/email-domains",
    response_model=EmailDomainResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_email_domain(
    party_id: UUID,
    body: EmailDomainCreate,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> EmailDomainResponse:
    row = await PartyService(session).create_email_domain(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=party_id,
        domain=body.domain,
        source_ref=body.source_ref,
    )
    await session.commit()
    return EmailDomainResponse.from_row(row)


@router.get("/{party_id}/charge-overrides", response_model=list[ChargeOverrideResponse])
async def list_charge_overrides(
    party_id: UUID,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ChargeOverrideResponse]:
    rows = await PartyService(session).list_charge_overrides(party_id)
    return [ChargeOverrideResponse.from_row(row) for row in rows]


@router.post(
    "/{party_id}/charge-overrides",
    response_model=ChargeOverrideResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_charge_override(
    party_id: UUID,
    body: ChargeOverrideCreate,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ChargeOverrideResponse:
    row = await PartyService(session).create_charge_override(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=party_id,
        charge_code=body.charge_code,
        amount=body.amount,
        currency=body.currency,
        lane_pattern=body.lane_pattern,
        basis=body.basis,
        source_ref=body.source_ref,
    )
    await session.commit()
    return ChargeOverrideResponse.from_row(row)


@router.get("/{party_id}/carrier-profile", response_model=CarrierProfileResponse | None)
async def get_carrier_profile(
    party_id: UUID,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> CarrierProfileResponse | None:
    row = await PartyService(session).get_carrier_profile(party_id)
    if row is None:
        return None
    return CarrierProfileResponse.from_row(row)


@router.put("/{party_id}/carrier-profile", response_model=CarrierProfileResponse)
async def upsert_carrier_profile(
    party_id: UUID,
    body: CarrierProfileUpsert,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CarrierProfileResponse:
    row = await PartyService(session).upsert_carrier_profile(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=party_id,
        scac_code=body.scac_code,
        is_nvocc=body.is_nvocc,
        rate_source_email=body.rate_source_email,
        api_adapter=body.api_adapter,
        dcsa_tnt_version=body.dcsa_tnt_version,
    )
    await session.commit()
    return CarrierProfileResponse.from_row(row)


class PartyScreenSanctions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sanctions_list_ref: str


@router.post("/{party_id}/screen-sanctions", response_model=PartyResponse)
async def screen_party_sanctions(
    party_id: UUID,
    body: PartyScreenSanctions,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> PartyResponse:
    row = await PartyService(session).screen_sanctions(
        party_id,
        body.sanctions_list_ref,
    )
    await session.commit()
    return PartyResponse.from_row(row)
