from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.routing_guide_match import RoutingGuideMatch
from app.services.routing_guide_matches.routing_guide_match_service import (
    RoutingGuideMatchService,
)

router = APIRouter(
    prefix="/routing-guide-matches",
    tags=["routing-guide-matches"],
)

_PERM = "can_manage_routing_guide_matches"


class RoutingGuideMatchCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    match_kind: str
    source_ref: str


class RoutingGuideMatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    match_kind: str
    source_ref: str


def _pack(saved: RoutingGuideMatch) -> RoutingGuideMatchResponse:
    return RoutingGuideMatchResponse.model_validate(saved)


@router.get("", response_model=list[RoutingGuideMatchResponse])
async def list_routing_guide_matches(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RoutingGuideMatchResponse]:
    packed = await RoutingGuideMatchService(session).list_marks()
    return [_pack(row) for row in packed]


@router.post(
    "",
    response_model=RoutingGuideMatchResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_routing_guide_match(
    body: RoutingGuideMatchCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RoutingGuideMatchResponse:
    saved = await RoutingGuideMatchService(session).persist_routing_guide_match(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        match_kind=body.match_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _pack(saved)
