from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.schedule_exception_mark import ScheduleExceptionMark
from app.services.schedule_exception_marks.schedule_exception_mark_service import (
    ScheduleExceptionMarkService,
)

router = APIRouter(prefix="/schedule-exception-marks", tags=["schedule-exception-marks"])

_PERM = "can_manage_schedule_exception_marks"


class ScheduleExceptionMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    exception_kind: str
    source_ref: str


class ScheduleExceptionMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    exception_kind: str
    source_ref: str


def _row(saved: ScheduleExceptionMark) -> ScheduleExceptionMarkResponse:
    return ScheduleExceptionMarkResponse.model_validate(saved)


@router.get("", response_model=list[ScheduleExceptionMarkResponse])
async def list_schedule_exception_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ScheduleExceptionMarkResponse]:
    packed = await ScheduleExceptionMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ScheduleExceptionMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_schedule_exception_mark(
    body: ScheduleExceptionMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ScheduleExceptionMarkResponse:
    saved = await ScheduleExceptionMarkService(session).persist_schedule_exception_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        exception_kind=body.exception_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
