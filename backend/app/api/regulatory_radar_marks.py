from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.regulatory_radar_mark import RegulatoryRadarMark
from app.services.regulatory_radar_marks.regulatory_radar_mark_service import (
    RegulatoryRadarMarkService,
)

router = APIRouter(prefix="/regulatory-radar-marks", tags=["regulatory-radar-marks"])

_PERM = "can_manage_regulatory_radar_marks"


class RegulatoryRadarMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    radar_kind: str
    source_ref: str


class RegulatoryRadarMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    radar_kind: str
    source_ref: str


def _row(saved: RegulatoryRadarMark) -> RegulatoryRadarMarkResponse:
    return RegulatoryRadarMarkResponse.model_validate(saved)


@router.get("", response_model=list[RegulatoryRadarMarkResponse])
async def list_regulatory_radar_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RegulatoryRadarMarkResponse]:
    packed = await RegulatoryRadarMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=RegulatoryRadarMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_regulatory_radar_mark(
    body: RegulatoryRadarMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RegulatoryRadarMarkResponse:
    saved = await RegulatoryRadarMarkService(session).persist_regulatory_radar_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        radar_kind=body.radar_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
