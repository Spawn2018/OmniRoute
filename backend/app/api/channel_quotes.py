from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.channel_quote import ChannelQuote
from app.repositories.channel_quotes.channel_quote_repository import ChannelQuoteCard
from app.services.channel_quotes.channel_quote_service import ChannelQuoteService

router = APIRouter(prefix="/channel-quotes", tags=["channel-quotes"])

_RATES = require_permission("can_manage_rate_lines", "organization")


class ChannelQuoteCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    party_id: UUID
    origin_port_id: UUID
    destination_port_id: UUID
    quote_date: date
    amount: str = Field(min_length=1, max_length=32)
    currency: str = Field(min_length=3, max_length=3)
    transit_days: int | None = None


class ChannelQuoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    party_id: UUID
    origin_port_id: UUID
    destination_port_id: UUID
    quote_date: date
    amount: str
    currency: str
    transit_days: int | None
    source_ref: str
    is_cheapest: bool
    is_fastest_tt: bool

    @classmethod
    def from_row(
        cls,
        row: ChannelQuote,
        *,
        is_cheapest: bool = False,
        is_fastest_tt: bool = False,
    ) -> "ChannelQuoteResponse":
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            party_id=row.party_id,
            origin_port_id=row.origin_port_id,
            destination_port_id=row.destination_port_id,
            quote_date=row.quote_date,
            amount=format(row.amount, "f"),
            currency=str(row.currency).strip(),
            transit_days=row.transit_days,
            source_ref=row.source_ref,
            is_cheapest=is_cheapest,
            is_fastest_tt=is_fastest_tt,
        )

    @classmethod
    def from_card(cls, card: ChannelQuoteCard) -> "ChannelQuoteResponse":
        return cls.from_row(
            card.quote,
            is_cheapest=card.is_cheapest,
            is_fastest_tt=card.is_fastest_tt,
        )


@router.get("", response_model=list[ChannelQuoteResponse])
async def list_channel_quotes(
    _authz: None = Depends(_RATES),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ChannelQuoteResponse]:
    service = ChannelQuoteService(session)
    cards = await service.list_quote_cards()
    return [ChannelQuoteResponse.from_card(card) for card in cards]


@router.get("/resolve", response_model=ChannelQuoteResponse)
async def resolve_channel_quote(
    party_id: UUID = Query(...),
    origin_port_id: UUID = Query(...),
    destination_port_id: UUID = Query(...),
    on_date: date = Query(...),
    _authz: None = Depends(_RATES),
    session: AsyncSession = Depends(require_tenant_session),
) -> ChannelQuoteResponse:
    service = ChannelQuoteService(session)
    row = await service.resolve(
        party_id=party_id,
        origin_port_id=origin_port_id,
        destination_port_id=destination_port_id,
        on_date=on_date,
    )
    return ChannelQuoteResponse.from_row(row)


@router.post("", response_model=ChannelQuoteResponse, status_code=status.HTTP_201_CREATED)
async def create_channel_quote(
    body: ChannelQuoteCreate,
    _authz: None = Depends(_RATES),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ChannelQuoteResponse:
    service = ChannelQuoteService(session)
    row = await service.create_quote(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=body.party_id,
        origin_port_id=body.origin_port_id,
        destination_port_id=body.destination_port_id,
        quote_date=body.quote_date,
        amount=body.amount,
        currency=body.currency,
        transit_days=body.transit_days,
    )
    await session.commit()
    return ChannelQuoteResponse.from_row(row)
