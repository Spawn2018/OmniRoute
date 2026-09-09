from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_bid_stance import TenderBidStance
from app.services.tender_bid_stances.tender_bid_stance_service import TenderBidStanceService
from app.services.tenders.tender_service import TenderService

router = APIRouter(prefix="/tender-bid-stances", tags=["tender-bid-stances"])

_PERM = "can_manage_tender_bid_stances"


class TenderBidStanceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tender_id: UUID
    stance_code: str
    source_ref: str


class TenderBidStanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    tender_id: UUID
    stance_code: str
    source_ref: str


def _as_row(row: TenderBidStance) -> TenderBidStanceResponse:
    return TenderBidStanceResponse(
        id=row.id,
        organization_id=row.organization_id,
        tender_id=row.tender_id,
        stance_code=row.stance_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderBidStanceResponse])
async def list_tender_bid_stances(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderBidStanceResponse]:
    rows = await TenderBidStanceService(session).list_stances()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=TenderBidStanceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tender_bid_stance(
    body: TenderBidStanceCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderBidStanceResponse:
    board = await TenderService(session).get_board(body.tender_id)
    row = await TenderBidStanceService(session).persist_stance(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        tender_id=board.id,
        stance_code=body.stance_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
