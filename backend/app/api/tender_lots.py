from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_lot import TenderLot
from app.services.tender_lots.tender_lot_service import TenderLotService
from app.services.tenders.tender_service import TenderService

router = APIRouter(prefix="/tender-lots", tags=["tender-lots"])

_PERM = "can_manage_tender_lots"


class TenderLotCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tender_id: UUID
    lot_code: str
    source_ref: str


class TenderLotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    tender_id: UUID
    lot_code: str
    source_ref: str


def _as_row(row: TenderLot) -> TenderLotResponse:
    return TenderLotResponse(
        id=row.id,
        organization_id=row.organization_id,
        tender_id=row.tender_id,
        lot_code=row.lot_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderLotResponse])
async def list_tender_lots(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderLotResponse]:
    rows = await TenderLotService(session).list_lots()
    return [_as_row(row) for row in rows]


@router.post("", response_model=TenderLotResponse, status_code=status.HTTP_201_CREATED)
async def create_tender_lot(
    body: TenderLotCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderLotResponse:
    board = await TenderService(session).get_board(body.tender_id)
    row = await TenderLotService(session).record_lot(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        tender_id=board.id,
        lot_code=body.lot_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
