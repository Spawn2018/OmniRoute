from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.shipment_stakeholder import ShipmentStakeholder
from app.services.parties.party_service import PartyService
from app.services.shipment_stakeholders.shipment_stakeholder_service import (
    ShipmentStakeholderService,
)
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/shipment-stakeholders", tags=["shipment-stakeholders"])


class ShipmentStakeholderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    party_id: UUID
    role: str
    source_ref: str


class ShipmentStakeholderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    party_id: UUID
    role: str
    source_ref: str
    superseded_by: UUID | None


def _as_response(row: ShipmentStakeholder) -> ShipmentStakeholderResponse:
    return ShipmentStakeholderResponse.model_validate(row)


@router.get("", response_model=list[ShipmentStakeholderResponse])
async def list_shipment_stakeholders(
    shipment_id: UUID = Query(...),
    _authz: None = Depends(require_permission("can_manage_shipments", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ShipmentStakeholderResponse]:
    await ShipmentService(session).get_shipment(shipment_id)
    rows = await ShipmentStakeholderService(session).list_for_shipment(shipment_id)
    return [_as_response(row) for row in rows]


@router.post(
    "",
    response_model=ShipmentStakeholderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_shipment_stakeholder(
    body: ShipmentStakeholderCreate,
    _authz: None = Depends(require_permission("can_manage_shipments", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipmentStakeholderResponse:
    shipment = await ShipmentService(session).get_shipment(body.shipment_id)
    party = await PartyService(session).get_party(body.party_id)
    row = await ShipmentStakeholderService(session).record_assignment(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=shipment.id,
        party_id=party.id,
        role=body.role,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(row)
