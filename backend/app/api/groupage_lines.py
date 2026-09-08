from datetime import time
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.groupage_line import require_distinct_line_ends, require_line_location_kind
from app.models.groupage_line import GroupageLine
from app.models.location import Location
from app.services.geography.location_service import LocationService
from app.services.groupage_lines.groupage_line_service import GroupageLineService

router = APIRouter(prefix="/groupage-lines", tags=["groupage-lines"])

_PERM = "can_manage_groupage_lines"


class GroupageLineCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    line_code: str
    origin_location_id: UUID
    destination_location_id: UUID
    cutoff_local: time
    transit_days: int
    operating_dows: list[int]
    source_ref: str


class GroupageLineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    line_code: str
    origin_location_id: UUID
    destination_location_id: UUID
    cutoff_local: time
    transit_days: int
    operating_dows: list[int]
    source_ref: str
    superseded_by: UUID | None


def _as_response(row: GroupageLine) -> GroupageLineResponse:
    return GroupageLineResponse.model_validate(row)


@router.get("", response_model=list[GroupageLineResponse])
async def list_groupage_lines(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[GroupageLineResponse]:
    rows = await GroupageLineService(session).list_lines()
    return [_as_response(row) for row in rows]


@router.post("", response_model=GroupageLineResponse, status_code=status.HTTP_201_CREATED)
async def create_groupage_line(
    body: GroupageLineCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> GroupageLineResponse:
    origin, destination = await _line_ends(
        session,
        body.origin_location_id,
        body.destination_location_id,
    )
    row = await GroupageLineService(session).record_line(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        line_code=body.line_code,
        origin_location_id=origin.id,
        destination_location_id=destination.id,
        cutoff_local=body.cutoff_local,
        transit_days=body.transit_days,
        operating_dows=body.operating_dows,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(row)


async def _line_ends(
    session: AsyncSession,
    origin_id: UUID,
    destination_id: UUID,
) -> tuple[Location, Location]:
    catalog = LocationService(session)
    origin = await catalog.get_location(origin_id)
    destination = await catalog.get_location(destination_id)
    require_line_location_kind(origin.kind)
    require_line_location_kind(destination.kind)
    require_distinct_line_ends(origin.id, destination.id)
    return origin, destination
