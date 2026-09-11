from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.routing_guide import RoutingGuide
from app.services.routing_guides.routing_guide_service import RoutingGuideService

router = APIRouter(prefix="/routing-guides", tags=["routing-guides"])

_PERM = "can_manage_routing_guides"


class RoutingGuideCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    guide_code: str
    lane_label: str | None = None
    mode_label: str | None = None
    source_ref: str


class RoutingGuideResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    guide_code: str
    lane_label: str | None
    mode_label: str | None
    source_ref: str


def _guide(saved: RoutingGuide) -> RoutingGuideResponse:
    return RoutingGuideResponse.model_validate(saved)


@router.get("", response_model=list[RoutingGuideResponse])
async def list_routing_guides(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RoutingGuideResponse]:
    packed = await RoutingGuideService(session).list_guides()
    return [_guide(item) for item in packed]


@router.post(
    "",
    response_model=RoutingGuideResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_routing_guide(
    body: RoutingGuideCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RoutingGuideResponse:
    saved = await RoutingGuideService(session).persist_routing_guide(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        guide_code=body.guide_code,
        lane_label=body.lane_label,
        mode_label=body.mode_label,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _guide(saved)
