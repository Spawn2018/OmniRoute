from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.ferry_booking_mark import FerryBookingMark
from app.services.ferry_booking_marks.ferry_booking_mark_service import (
    FerryBookingMarkService,
)

router = APIRouter(prefix="/ferry-booking-marks", tags=["ferry-booking-marks"])

_PERM = "can_manage_ferry_booking_marks"


class FerryBookingMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    booking_kind: str
    source_ref: str


class FerryBookingMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    booking_kind: str
    source_ref: str


def _row(saved: FerryBookingMark) -> FerryBookingMarkResponse:
    return FerryBookingMarkResponse.model_validate(saved)


@router.get("", response_model=list[FerryBookingMarkResponse])
async def list_ferry_booking_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FerryBookingMarkResponse]:
    packed = await FerryBookingMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=FerryBookingMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ferry_booking_mark(
    body: FerryBookingMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FerryBookingMarkResponse:
    saved = await FerryBookingMarkService(session).persist_ferry_booking_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        booking_kind=body.booking_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
