from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.consignment import (
    parse_optional_load_kind,
    require_consignment_shipment_id,
    require_ftl_room,
)
from app.models.consignment import Consignment
from app.repositories.consignments.consignment_repository import ConsignmentRepository
from app.services.consignments.consignment_service import ConsignmentService
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/consignments", tags=["consignments"])

_PERM = "can_manage_consignments"


class ConsignmentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID | bool | None = None
    consignment_ref: str
    source_ref: str
    # 540.0: tylko egzekucja FTL=1 — nie kolumna na shipment
    load_kind: Literal["ftl", "ltl"] | None = None


class ConsignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    consignment_ref: str
    source_ref: str


def _as_row(row: Consignment) -> ConsignmentResponse:
    return ConsignmentResponse.model_validate(row)


@router.get("", response_model=list[ConsignmentResponse])
async def list_consignments(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ConsignmentResponse]:
    rows = await ConsignmentService(session).list_parcels()
    return [_as_row(row) for row in rows]


@router.post("", response_model=ConsignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_consignment(
    body: ConsignmentCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ConsignmentResponse:
    shipment_id = require_consignment_shipment_id(body.shipment_id)
    order = await ShipmentService(session).get_shipment(shipment_id)
    kind = parse_optional_load_kind(body.load_kind)
    if kind == "ftl":
        existing = await ConsignmentRepository(session).count_for_shipment(order.id)
        require_ftl_room(existing)
    row = await ConsignmentService(session).record_parcel(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=order.id,
        consignment_ref=body.consignment_ref,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
