from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.calibration_mark import CalibrationMark
from app.services.calibration_marks.calibration_mark_service import (
    CalibrationMarkService,
)

router = APIRouter(prefix="/calibration-marks", tags=["calibration-marks"])

_PERM = "can_manage_calibration_marks"


class CalibrationMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    sample_ready: str
    source_ref: str


class CalibrationMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    sample_ready: str
    source_ref: str


def _mark(saved: CalibrationMark) -> CalibrationMarkResponse:
    return CalibrationMarkResponse.model_validate(saved)


@router.get("", response_model=list[CalibrationMarkResponse])
async def list_calibration_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CalibrationMarkResponse]:
    packed = await CalibrationMarkService(session).list_marks()
    return [_mark(item) for item in packed]


@router.post(
    "",
    response_model=CalibrationMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_calibration_mark(
    body: CalibrationMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CalibrationMarkResponse:
    saved = await CalibrationMarkService(session).persist_calibration_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        sample_ready=body.sample_ready,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _mark(saved)
