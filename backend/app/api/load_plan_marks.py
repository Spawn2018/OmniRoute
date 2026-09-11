from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.load_plan_mark import LoadPlanMark
from app.services.load_plan_marks.load_plan_mark_service import LoadPlanMarkService

router = APIRouter(prefix="/load-plan-marks", tags=["load-plan-marks"])

_PERM = "can_manage_load_plan_marks"


class LoadPlanMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    stance_kind: str
    source_ref: str


class LoadPlanMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    stance_kind: str
    source_ref: str


def _row(saved: LoadPlanMark) -> LoadPlanMarkResponse:
    return LoadPlanMarkResponse.model_validate(saved)


@router.get("", response_model=list[LoadPlanMarkResponse])
async def list_load_plan_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LoadPlanMarkResponse]:
    packed = await LoadPlanMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=LoadPlanMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_load_plan_mark(
    body: LoadPlanMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LoadPlanMarkResponse:
    saved = await LoadPlanMarkService(session).persist_load_plan_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        stance_kind=body.stance_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
