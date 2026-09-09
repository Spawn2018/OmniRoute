from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.free_time_clock import FreeTimeClock
from app.services.free_time_clocks.free_time_clock_service import FreeTimeClockService

router = APIRouter(prefix="/free-time-clocks", tags=["free-time-clocks"])

_PERM = "can_manage_free_time_clocks"


class FreeTimeClockCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    clock_kind: str
    free_days: int
    source_ref: str


class FreeTimeClockResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    clock_kind: str
    free_days: int
    source_ref: str


def _as_row(row: FreeTimeClock) -> FreeTimeClockResponse:
    return FreeTimeClockResponse.model_validate(row)


@router.get("", response_model=list[FreeTimeClockResponse])
async def list_free_time_clocks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FreeTimeClockResponse]:
    rows = await FreeTimeClockService(session).list_marks()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=FreeTimeClockResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_free_time_clock(
    body: FreeTimeClockCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FreeTimeClockResponse:
    row = await FreeTimeClockService(session).persist_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        clock_kind=body.clock_kind,
        free_days=body.free_days,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
