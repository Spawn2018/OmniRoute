from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.route_plan_mark import RoutePlanMark
from app.services.route_plan_marks.route_plan_mark_service import RoutePlanMarkService

router = APIRouter(prefix="/route-plan-marks", tags=["route-plan-marks"])

_PERM = "can_manage_route_plan_marks"


class RoutePlanMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    plan_kind: str
    source_ref: str


class RoutePlanMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    plan_kind: str
    source_ref: str


def _row(saved: RoutePlanMark) -> RoutePlanMarkResponse:
    return RoutePlanMarkResponse.model_validate(saved)


@router.get("", response_model=list[RoutePlanMarkResponse])
async def list_route_plan_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RoutePlanMarkResponse]:
    packed = await RoutePlanMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=RoutePlanMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_route_plan_mark(
    body: RoutePlanMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RoutePlanMarkResponse:
    saved = await RoutePlanMarkService(session).persist_route_plan_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        plan_kind=body.plan_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
