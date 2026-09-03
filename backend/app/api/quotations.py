from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.customer_rfq import inherit_rfq_commodity_code_id, require_rfq_party
from app.domain.money import Money
from app.models.customer_rfq import CustomerRfq
from app.models.quotation import Quotation
from app.services.channel_quotes.channel_quote_service import ChannelQuoteService
from app.services.commodity_codes.commodity_code_service import CommodityCodeService
from app.services.customer_rfqs.customer_rfq_service import CustomerRfqService
from app.services.organization_settings.organization_setting_service import (
    OrganizationSettingService,
)
from app.services.quotations.quotation_service import QuotationService

router = APIRouter(prefix="/quotations", tags=["quotations"])


class QuotationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    charge_code: str = Field(min_length=1, max_length=32)
    origin_port_id: UUID
    destination_port_id: UUID
    party_id: UUID
    customer_rfq_id: UUID | None = None
    commodity_code_id: UUID | None = None


class QuotationBatchCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    charge_codes: list[str] = Field(min_length=1, max_length=20)
    origin_port_id: UUID
    destination_port_id: UUID
    party_id: UUID
    customer_rfq_id: UUID | None = None
    commodity_code_id: UUID | None = None


class QuotationResponse(BaseModel):
    id: UUID
    organization_id: UUID
    charge_code: str
    rate_line_id: UUID
    amount: str
    currency: str
    source_ref: str
    origin_port_id: UUID | None
    destination_port_id: UUID | None
    party_id: UUID | None
    customer_rfq_id: UUID | None
    commodity_code_id: UUID | None
    document_number: str | None
    negotiated_channel_quote_id: UUID | None

    @classmethod
    def from_row(cls, row: Quotation) -> "QuotationResponse":
        money = Money.of(row.amount, row.currency)
        amount_text, currency = money.as_pair()
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            charge_code=row.charge_code,
            rate_line_id=row.rate_line_id,
            amount=amount_text,
            currency=currency,
            source_ref=row.source_ref,
            origin_port_id=row.origin_port_id,
            destination_port_id=row.destination_port_id,
            party_id=row.party_id,
            customer_rfq_id=row.customer_rfq_id,
            commodity_code_id=row.commodity_code_id,
            document_number=row.document_number,
            negotiated_channel_quote_id=row.negotiated_channel_quote_id,
        )


class QuotationNegotiate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    channel_quote_id: UUID


class QuotationDocumentLayout(BaseModel):
    prefix: str | None
    print_template: str


async def _loaded_quote_rfq(
    session: AsyncSession,
    customer_rfq_id: UUID | None,
    party_id: UUID,
) -> CustomerRfq | None:
    if customer_rfq_id is None:
        return None
    rfq = await CustomerRfqService(session).get_rfq(customer_rfq_id)
    require_rfq_party(rfq.party_id, party_id)
    return rfq


async def _quote_commodity_code_id(
    session: AsyncSession,
    selected: UUID | None,
    rfq: CustomerRfq | None,
) -> UUID | None:
    inherited = inherit_rfq_commodity_code_id(
        selected,
        None if rfq is None else rfq.commodity_code_id,
    )
    if inherited is None:
        return None
    found = await CommodityCodeService(session).get_code(inherited)
    return found.id


@router.get("", response_model=list[QuotationResponse])
async def list_quotations(
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    party_id: UUID | None = Query(default=None),
    origin_port_id: UUID | None = Query(default=None),
    destination_port_id: UUID | None = Query(default=None),
    customer_rfq_id: UUID | None = Query(default=None),
) -> list[QuotationResponse]:
    service = QuotationService(session)
    rows = await service.list_quotations(
        party_id=party_id,
        origin_port_id=origin_port_id,
        destination_port_id=destination_port_id,
        customer_rfq_id=customer_rfq_id,
    )
    return [QuotationResponse.from_row(row) for row in rows]


@router.post("", response_model=QuotationResponse, status_code=status.HTTP_201_CREATED)
async def create_quotation(
    body: QuotationCreate,
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> QuotationResponse:
    service = QuotationService(session)
    rfq = await _loaded_quote_rfq(session, body.customer_rfq_id, body.party_id)
    linked_hs = await _quote_commodity_code_id(session, body.commodity_code_id, rfq)
    row = await service.quote_from_current_rate(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        charge_code=body.charge_code,
        origin_port_id=body.origin_port_id,
        destination_port_id=body.destination_port_id,
        party_id=body.party_id,
        customer_rfq_id=None if rfq is None else rfq.id,
        commodity_code_id=linked_hs,
    )
    await session.commit()
    return QuotationResponse.from_row(row)


@router.post("/batch", response_model=list[QuotationResponse], status_code=status.HTTP_201_CREATED)
async def create_quotation_batch(
    body: QuotationBatchCreate,
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> list[QuotationResponse]:
    service = QuotationService(session)
    rfq = await _loaded_quote_rfq(session, body.customer_rfq_id, body.party_id)
    linked_hs = await _quote_commodity_code_id(session, body.commodity_code_id, rfq)
    rows = await service.quote_batch_from_current_rates(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        charge_codes=body.charge_codes,
        origin_port_id=body.origin_port_id,
        destination_port_id=body.destination_port_id,
        party_id=body.party_id,
        customer_rfq_id=None if rfq is None else rfq.id,
        commodity_code_id=linked_hs,
    )
    await session.commit()
    return [QuotationResponse.from_row(row) for row in rows]


async def _quotation_prefix(session: AsyncSession) -> str | None:
    row = await OrganizationSettingService(session).get_setting("quotation_number_prefix")
    if row is None:
        return None
    return row.setting_value


async def _quotation_print_template(session: AsyncSession) -> str:
    row = await OrganizationSettingService(session).get_setting("quotation_print_template")
    if row is None:
        return "plain"
    return row.setting_value


@router.get("/document-layout", response_model=QuotationDocumentLayout)
async def quotation_document_layout(
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> QuotationDocumentLayout:
    return QuotationDocumentLayout(
        prefix=await _quotation_prefix(session),
        print_template=await _quotation_print_template(session),
    )


@router.patch("/{quotation_id}/negotiate", response_model=QuotationResponse)
async def negotiate_quotation(
    quotation_id: UUID,
    body: QuotationNegotiate,
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> QuotationResponse:
    await ChannelQuoteService(session).get_quote(body.channel_quote_id)
    row = await QuotationService(session).set_negotiated_channel_quote(
        quotation_id,
        body.channel_quote_id,
    )
    await session.commit()
    return QuotationResponse.from_row(row)


@router.post("/{quotation_id}/document-number", response_model=QuotationResponse)
async def issue_quotation_document_number(
    quotation_id: UUID,
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> QuotationResponse:
    row = await QuotationService(session).issue_document_number(
        quotation_id=quotation_id,
        prefix=await _quotation_prefix(session),
    )
    await session.commit()
    return QuotationResponse.from_row(row)
