from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.plan_snapshot import PlanSnapshot
from app.services.plan_snapshots.plan_snapshot_service import PlanSnapshotService

router = APIRouter(prefix="/plan-snapshots", tags=["plan-snapshots"])

_PERM = "can_manage_plan_snapshots"


class PlanSnapshotCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    snapshot_code: str
    shipment_id: str
    trip_id: str
    resource_id: str
    author_label: str
    recorded_at: str
    source_ref: str


class PlanSnapshotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    snapshot_code: str
    shipment_id: UUID
    trip_id: UUID
    resource_id: UUID
    author_label: str
    recorded_at: datetime
    source_ref: str


def _as_row(row: PlanSnapshot) -> PlanSnapshotResponse:
    return PlanSnapshotResponse.model_validate(row)


@router.get("", response_model=list[PlanSnapshotResponse])
async def list_plan_snapshots(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PlanSnapshotResponse]:
    rows = await PlanSnapshotService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=PlanSnapshotResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_plan_snapshot(
    body: PlanSnapshotCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PlanSnapshotResponse:
    row = await PlanSnapshotService(session).persist_snapshot(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        snapshot_code=body.snapshot_code,
        shipment_id=body.shipment_id,
        trip_id=body.trip_id,
        resource_id=body.resource_id,
        author_label=body.author_label,
        recorded_at=body.recorded_at,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
