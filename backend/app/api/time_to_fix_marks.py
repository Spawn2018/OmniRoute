from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.time_to_fix_mark import TimeToFixMark
from app.services.time_to_fix_marks.time_to_fix_mark_service import (
    TimeToFixMarkService,
)

router = APIRouter(prefix="/time-to-fix-marks", tags=["time-to-fix-marks"])

_PERM = "can_manage_time_to_fix_marks"


class TimeToFixMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    fix_kind: str
    source_ref: str


class TimeToFixMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    fix_kind: str
    source_ref: str


def _row(saved: TimeToFixMark) -> TimeToFixMarkResponse:
    return TimeToFixMarkResponse.model_validate(saved)


@router.get("", response_model=list[TimeToFixMarkResponse])
async def list_time_to_fix_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TimeToFixMarkResponse]:
    packed = await TimeToFixMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=TimeToFixMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_time_to_fix_mark(
    body: TimeToFixMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TimeToFixMarkResponse:
    saved = await TimeToFixMarkService(session).persist_time_to_fix_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        fix_kind=body.fix_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
