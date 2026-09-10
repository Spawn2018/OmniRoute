from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.lane_km import LaneKm
from app.services.lane_kms.lane_km_service import LaneKmService

router = APIRouter(prefix="/lane-kms", tags=["lane-kms"])

_PERM = "can_manage_lane_kms"


class LaneKmCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    km_code: str
    loaded_km: str | int | float | bool
    empty_km: str | int | float | bool
    approach_km: str | int | float | bool
    source_ref: str


class LaneKmResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    km_code: str
    loaded_km: str
    empty_km: str
    approach_km: str
    source_ref: str


def _as_row(row: LaneKm) -> LaneKmResponse:
    return LaneKmResponse(
        id=row.id,
        organization_id=row.organization_id,
        km_code=row.km_code,
        loaded_km=format(row.loaded_km, "f"),
        empty_km=format(row.empty_km, "f"),
        approach_km=format(row.approach_km, "f"),
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[LaneKmResponse])
async def list_lane_kms(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LaneKmResponse]:
    rows = await LaneKmService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=LaneKmResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_lane_km(
    body: LaneKmCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LaneKmResponse:
    row = await LaneKmService(session).persist_lane_km(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        km_code=body.km_code,
        loaded_km=body.loaded_km,
        empty_km=body.empty_km,
        approach_km=body.approach_km,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
