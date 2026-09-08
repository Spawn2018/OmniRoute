from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.party_lane_scorecard import lane_scorecard_hint
from app.models.party_lane_scorecard import PartyLaneScorecard
from app.services.parties.party_service import PartyService

router = APIRouter(prefix="/party-lane-scorecards", tags=["party-lane-scorecards"])

_PARTIES = require_permission("can_manage_parties", "organization")


class LaneScorecardUpsert(BaseModel):
    model_config = ConfigDict(extra="forbid")

    party_id: UUID
    origin_port_id: UUID
    destination_port_id: UUID
    window_days: int | None = None
    sample_size: int = 0
    answered_inquiry_count: int = 0
    shipment_count: int = 0
    cheapest_count: int = 0
    median_response_hours: str | None = None


class LaneScorecardResponse(BaseModel):
    id: UUID
    organization_id: UUID
    party_id: UUID
    origin_port_id: UUID
    destination_port_id: UUID
    window_days: int
    sample_size: int
    answered_inquiry_count: int
    shipment_count: int
    cheapest_count: int
    median_response_hours: str | None
    computed_at: datetime
    source_ref: str
    hint: str

    @classmethod
    def from_row(cls, row: PartyLaneScorecard) -> "LaneScorecardResponse":
        hours = row.median_response_hours
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            party_id=row.party_id,
            origin_port_id=row.origin_port_id,
            destination_port_id=row.destination_port_id,
            window_days=row.window_days,
            sample_size=row.sample_size,
            answered_inquiry_count=row.answered_inquiry_count,
            shipment_count=row.shipment_count,
            cheapest_count=row.cheapest_count,
            median_response_hours=None if hours is None else format(hours, "f"),
            computed_at=row.computed_at,
            source_ref=row.source_ref,
            hint=lane_scorecard_hint(
                sample_size=row.sample_size,
                answered_inquiry_count=row.answered_inquiry_count,
                shipment_count=row.shipment_count,
                cheapest_count=row.cheapest_count,
                median_response_hours=hours if isinstance(hours, Decimal) else None,
                window_days=row.window_days,
            ),
        )


@router.get("", response_model=list[LaneScorecardResponse])
async def list_lane_scorecards(
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LaneScorecardResponse]:
    rows = await PartyService(session).list_lane_scorecards()
    return [LaneScorecardResponse.from_row(row) for row in rows]


@router.post("", response_model=LaneScorecardResponse, status_code=status.HTTP_200_OK)
async def upsert_lane_scorecard(
    body: LaneScorecardUpsert,
    _authz: None = Depends(_PARTIES),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LaneScorecardResponse:
    row = await PartyService(session).upsert_lane_scorecard(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=body.party_id,
        origin_port_id=body.origin_port_id,
        destination_port_id=body.destination_port_id,
        window_days=body.window_days,
        sample_size=body.sample_size,
        answered_inquiry_count=body.answered_inquiry_count,
        shipment_count=body.shipment_count,
        cheapest_count=body.cheapest_count,
        median_response_hours=body.median_response_hours,
    )
    await session.commit()
    return LaneScorecardResponse.from_row(row)
