from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.sales_lane import SalesLane
from app.services.sales_lanes.sales_lane_service import SalesLaneService

router = APIRouter(prefix="/sales-lanes", tags=["sales-lanes"])

_PERM = "can_manage_sales_lanes"


class SalesLaneCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lane_code: str
    lane_kind: str
    source_ref: str


class SalesLaneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    lane_code: str
    lane_kind: str
    source_ref: str


def _row(saved: SalesLane) -> SalesLaneResponse:
    return SalesLaneResponse.model_validate(saved)


@router.get("", response_model=list[SalesLaneResponse])
async def list_sales_lanes(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SalesLaneResponse]:
    packed = await SalesLaneService(session).list_lanes()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=SalesLaneResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_sales_lane(
    body: SalesLaneCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SalesLaneResponse:
    saved = await SalesLaneService(session).persist_sales_lane(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        lane_code=body.lane_code,
        lane_kind=body.lane_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
