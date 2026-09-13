from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tacho_plan_mark import TachoPlanMark
from app.services.tacho_plan_marks.tacho_plan_mark_service import TachoPlanMarkService

router = APIRouter(prefix="/tacho-plan-marks", tags=["tacho-plan-marks"])

_PERM = "can_manage_tacho_plan_marks"


class TachoPlanMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    constraint_kind: str
    source_ref: str


class TachoPlanMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    constraint_kind: str
    source_ref: str


def _row(saved: TachoPlanMark) -> TachoPlanMarkResponse:
    return TachoPlanMarkResponse.model_validate(saved)


@router.get("", response_model=list[TachoPlanMarkResponse])
async def list_tacho_plan_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TachoPlanMarkResponse]:
    packed = await TachoPlanMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=TachoPlanMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tacho_plan_mark(
    body: TachoPlanMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TachoPlanMarkResponse:
    saved = await TachoPlanMarkService(session).persist_tacho_plan_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        constraint_kind=body.constraint_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
