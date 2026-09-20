from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.stop_group import require_stop_group_shipment_id
from app.models.stop_group import StopGroup
from app.services.shipments.shipment_service import ShipmentService
from app.services.stop_groups.stop_group_service import StopGroupService

router = APIRouter(prefix="/stop-groups", tags=["stop-groups"])

_PERM = "can_manage_shipments"


class StopGroupCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID | bool | None = None
    group_code: str
    source_ref: str


class StopGroupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    group_code: str
    source_ref: str


def _as_row(row: StopGroup) -> StopGroupResponse:
    return StopGroupResponse.model_validate(row)


@router.get("", response_model=list[StopGroupResponse])
async def list_stop_groups(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[StopGroupResponse]:
    rows = await StopGroupService(session).list_groups()
    return [_as_row(row) for row in rows]


@router.post("", response_model=StopGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_stop_group(
    body: StopGroupCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> StopGroupResponse:
    shipment_id = require_stop_group_shipment_id(body.shipment_id)
    order = await ShipmentService(session).get_shipment(shipment_id)
    row = await StopGroupService(session).record_group(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=order.id,
        group_code=body.group_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
