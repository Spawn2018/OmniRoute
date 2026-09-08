from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.booking_instruction import BookingInstruction
from app.services.booking_instructions.booking_instruction_service import (
    BookingInstructionService,
)
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/booking-instructions", tags=["booking-instructions"])


class BookingInstructionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    booking_scope: str
    target_role: str
    status: str
    source_ref: str


class BookingInstructionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    booking_scope: str
    target_role: str
    status: str
    source_ref: str
    superseded_by: UUID | None


def _as_response(row: BookingInstruction) -> BookingInstructionResponse:
    return BookingInstructionResponse.model_validate(row)


@router.get("", response_model=list[BookingInstructionResponse])
async def list_booking_instructions(
    shipment_id: UUID = Query(...),
    _authz: None = Depends(require_permission("can_manage_shipments", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[BookingInstructionResponse]:
    await ShipmentService(session).get_shipment(shipment_id)
    rows = await BookingInstructionService(session).list_for_shipment(shipment_id)
    return [_as_response(row) for row in rows]


@router.post(
    "",
    response_model=BookingInstructionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking_instruction(
    body: BookingInstructionCreate,
    _authz: None = Depends(require_permission("can_manage_shipments", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> BookingInstructionResponse:
    shipment = await ShipmentService(session).get_shipment(body.shipment_id)
    row = await BookingInstructionService(session).record_instruction(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=shipment.id,
        booking_scope=body.booking_scope,
        target_role=body.target_role,
        status=body.status,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(row)
