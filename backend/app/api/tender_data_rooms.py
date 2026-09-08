from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_data_room import TenderDataRoom
from app.services.tender_data_rooms.tender_data_room_service import TenderDataRoomService
from app.services.tenders.tender_service import TenderService

router = APIRouter(prefix="/tender-data-rooms", tags=["tender-data-rooms"])

_PERM = "can_manage_tender_data_rooms"


class TenderDataRoomCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tender_id: UUID
    nda_mark: str
    source_ref: str


class TenderDataRoomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    tender_id: UUID
    nda_mark: str
    source_ref: str


def _as_row(row: TenderDataRoom) -> TenderDataRoomResponse:
    return TenderDataRoomResponse(
        id=row.id,
        organization_id=row.organization_id,
        tender_id=row.tender_id,
        nda_mark=row.nda_mark,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderDataRoomResponse])
async def list_tender_data_rooms(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderDataRoomResponse]:
    rows = await TenderDataRoomService(session).list_rooms()
    return [_as_row(row) for row in rows]


@router.post("", response_model=TenderDataRoomResponse, status_code=status.HTTP_201_CREATED)
async def create_tender_data_room(
    body: TenderDataRoomCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderDataRoomResponse:
    board = await TenderService(session).get_board(body.tender_id)
    row = await TenderDataRoomService(session).record_room(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        tender_id=board.id,
        nda_mark=body.nda_mark,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
