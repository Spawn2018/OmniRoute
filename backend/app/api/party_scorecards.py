from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.party_scorecard import PartyScorecard
from app.services.parties.party_service import PartyService

router = APIRouter(prefix="/party-scorecards", tags=["party-scorecards"])

_PARTIES = require_permission("can_manage_parties", "organization")


class ScorecardUpsert(BaseModel):
    model_config = ConfigDict(extra="forbid")

    response_rate: str | None = None
    median_response_hours: str | None = None
    price_position: str | None = None
    quote_invoice_match_rate: str | None = None
    rollover_count: int | None = None
    sample_size: int = 0
    window_days: int = Field(default=90, gt=0)


class ScorecardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    party_id: UUID
    response_rate: str | None
    median_response_hours: str | None
    price_position: str | None
    quote_invoice_match_rate: str | None
    rollover_count: int | None
    sample_size: int
    window_days: int
    computed_at: datetime
    source_ref: str

    @classmethod
    def from_row(cls, row: PartyScorecard) -> "ScorecardResponse":
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            party_id=row.party_id,
            response_rate=_dec(row.response_rate),
            median_response_hours=_dec(row.median_response_hours),
            price_position=_dec(row.price_position),
            quote_invoice_match_rate=_dec(row.quote_invoice_match_rate),
            rollover_count=row.rollover_count,
            sample_size=row.sample_size,
            window_days=row.window_days,
            computed_at=row.computed_at,
            source_ref=row.source_ref,
        )


def _dec(value: Decimal | None) -> str | None:
    return None if value is None else format(value, "f")


@router.get("", response_model=list[ScorecardResponse])
async def list_scorecards(
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ScorecardResponse]:
    service = PartyService(session)
    rows = await service.list_scorecards()
    return [ScorecardResponse.from_row(row) for row in rows]


@router.get("/{party_id}", response_model=ScorecardResponse)
async def get_scorecard(
    party_id: UUID,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> ScorecardResponse:
    service = PartyService(session)
    row = await service.get_scorecard(party_id)
    return ScorecardResponse.from_row(row)


@router.post("/{party_id}", response_model=ScorecardResponse, status_code=status.HTTP_200_OK)
async def upsert_scorecard(
    party_id: UUID,
    body: ScorecardUpsert,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ScorecardResponse:
    service = PartyService(session)
    row = await service.upsert_scorecard(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=party_id,
        response_rate=body.response_rate,
        median_response_hours=body.median_response_hours,
        price_position=body.price_position,
        quote_invoice_match_rate=body.quote_invoice_match_rate,
        rollover_count=body.rollover_count,
        sample_size=body.sample_size,
        window_days=body.window_days,
    )
    await session.commit()
    return ScorecardResponse.from_row(row)
