from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.rfid_mark import RfidMark
from app.services.rfid_marks.rfid_mark_service import RfidMarkService

router = APIRouter(prefix="/rfid-marks", tags=["rfid-marks"])

_PERM = "can_manage_rfid_marks"


class RfidMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    rfid_kind: str
    source_ref: str


class RfidMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    rfid_kind: str
    source_ref: str


def _row(saved: RfidMark) -> RfidMarkResponse:
    return RfidMarkResponse.model_validate(saved)


@router.get("", response_model=list[RfidMarkResponse])
async def list_rfid_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RfidMarkResponse]:
    packed = await RfidMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=RfidMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_rfid_mark(
    body: RfidMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RfidMarkResponse:
    saved = await RfidMarkService(session).persist_rfid_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        rfid_kind=body.rfid_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
