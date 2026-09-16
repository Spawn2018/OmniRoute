from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.trip_bill_mark import TripBillMark
from app.services.trip_bill_marks.trip_bill_mark_service import (
    TripBillMarkService,
)

router = APIRouter(
    prefix="/trip-bill-marks",
    tags=["trip-bill-marks"],
)

_PERM = "can_manage_trip_bill_marks"


class TripBillMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    bill_kind: str
    source_ref: str


class TripBillMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    bill_kind: str
    source_ref: str


def _row(saved: TripBillMark) -> TripBillMarkResponse:
    return TripBillMarkResponse.model_validate(saved)


@router.get("", response_model=list[TripBillMarkResponse])
async def list_trip_bill_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TripBillMarkResponse]:
    packed = await TripBillMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=TripBillMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_trip_bill_mark(
    body: TripBillMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TripBillMarkResponse:
    saved = await TripBillMarkService(session).persist_trip_bill_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        bill_kind=body.bill_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
