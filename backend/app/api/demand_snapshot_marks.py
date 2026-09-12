from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.demand_snapshot_mark import DemandSnapshotMark
from app.services.demand_snapshot_marks.demand_snapshot_mark_service import (
    DemandSnapshotMarkService,
)

router = APIRouter(prefix="/demand-snapshot-marks", tags=["demand-snapshot-marks"])

_RELATION = "can_manage_demand_snapshot_marks"


class DemandSnapshotMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    snapshot_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class DemandSnapshotMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    snapshot_kind: str
    source_ref: str


def _as_response(row: DemandSnapshotMark) -> DemandSnapshotMarkResponse:
    return DemandSnapshotMarkResponse.model_validate(row)


@router.get("", response_model=list[DemandSnapshotMarkResponse])
async def list_demand_snapshot_marks(
    _authz: None = Depends(require_permission(_RELATION, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[DemandSnapshotMarkResponse]:
    service = DemandSnapshotMarkService(session)
    return [_as_response(row) for row in await service.list_marks()]


@router.post(
    "",
    response_model=DemandSnapshotMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_demand_snapshot_mark(
    body: DemandSnapshotMarkCreate,
    _authz: None = Depends(require_permission(_RELATION, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> DemandSnapshotMarkResponse:
    service = DemandSnapshotMarkService(session)
    saved = await service.persist_demand_snapshot_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        snapshot_kind=body.snapshot_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(saved)
