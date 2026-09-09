from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.lane_pattern import LanePattern
from app.services.lane_patterns.lane_pattern_service import LanePatternService

router = APIRouter(prefix="/lane-patterns", tags=["lane-patterns"])

_PERM = "can_manage_lane_patterns"


class LanePatternCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    origin_unlocode: str
    destination_unlocode: str
    source_ref: str


class LanePatternResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    origin_unlocode: str
    destination_unlocode: str
    source_ref: str


def _as_row(row: LanePattern) -> LanePatternResponse:
    return LanePatternResponse(
        id=row.id,
        organization_id=row.organization_id,
        origin_unlocode=row.origin_unlocode,
        destination_unlocode=row.destination_unlocode,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[LanePatternResponse])
async def list_lane_patterns(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LanePatternResponse]:
    rows = await LanePatternService(session).list_patterns()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=LanePatternResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_lane_pattern(
    body: LanePatternCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LanePatternResponse:
    row = await LanePatternService(session).persist_pattern(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        origin_unlocode=body.origin_unlocode,
        destination_unlocode=body.destination_unlocode,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
