from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.routing_guide_enforcement import RoutingGuideEnforcement
from app.services.routing_guide_enforcements.routing_guide_enforcement_service import (
    RoutingGuideEnforcementService,
)

router = APIRouter(
    prefix="/routing-guide-enforcements",
    tags=["routing-guide-enforcements"],
)

_PERM = "can_manage_routing_guide_enforcements"


class RoutingGuideEnforcementCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    enforcement_kind: str
    source_ref: str


class RoutingGuideEnforcementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    enforcement_kind: str
    source_ref: str


def _pack(saved: RoutingGuideEnforcement) -> RoutingGuideEnforcementResponse:
    return RoutingGuideEnforcementResponse.model_validate(saved)


@router.get("", response_model=list[RoutingGuideEnforcementResponse])
async def list_routing_guide_enforcements(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RoutingGuideEnforcementResponse]:
    packed = await RoutingGuideEnforcementService(session).list_marks()
    return [_pack(row) for row in packed]


@router.post(
    "",
    response_model=RoutingGuideEnforcementResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_routing_guide_enforcement(
    body: RoutingGuideEnforcementCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RoutingGuideEnforcementResponse:
    saved = await RoutingGuideEnforcementService(
        session
    ).persist_routing_guide_enforcement(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        enforcement_kind=body.enforcement_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _pack(saved)
