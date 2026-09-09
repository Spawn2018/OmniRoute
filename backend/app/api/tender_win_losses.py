from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_win_loss import TenderWinLoss
from app.services.tender_win_losses.tender_win_loss_service import TenderWinLossService
from app.services.tenders.tender_service import TenderService

router = APIRouter(prefix="/tender-win-losses", tags=["tender-win-losses"])

_PERM = "can_manage_tender_win_losses"


class TenderWinLossCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tender_id: UUID
    outcome: str
    reason_code: str
    source_ref: str


class TenderWinLossResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    tender_id: UUID
    outcome: str
    reason_code: str
    source_ref: str


def _as_row(row: TenderWinLoss) -> TenderWinLossResponse:
    return TenderWinLossResponse(
        id=row.id,
        organization_id=row.organization_id,
        tender_id=row.tender_id,
        outcome=row.outcome,
        reason_code=row.reason_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderWinLossResponse])
async def list_tender_win_losses(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderWinLossResponse]:
    rows = await TenderWinLossService(session).list_verdicts()
    return [_as_row(row) for row in rows]


@router.post("", response_model=TenderWinLossResponse, status_code=status.HTTP_201_CREATED)
async def create_tender_win_loss(
    body: TenderWinLossCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderWinLossResponse:
    board = await TenderService(session).get_board(body.tender_id)
    row = await TenderWinLossService(session).record_verdict(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        tender_id=board.id,
        outcome=body.outcome,
        reason_code=body.reason_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
