from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.errors import InvalidFieldCarryForward
from app.services.field_carry_forwards.field_carry_forward_service import (
    FieldCarryForwardService,
)
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/field-carry-forwards", tags=["field-carry-forwards"])


class FieldCarryForwardCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quotation_id: UUID
    shipment_id: UUID
    fields: dict[str, str]


class FieldCarryForwardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    quotation_id: UUID
    shipment_id: UUID
    field_key: str
    field_value: str
    superseded_by: UUID | None


@router.get("", response_model=list[FieldCarryForwardResponse])
async def list_field_carry_forwards(
    shipment_id: UUID = Query(...),
    _authz: None = Depends(require_permission("can_manage_shipments", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FieldCarryForwardResponse]:
    rows = await FieldCarryForwardService(session).list_for_shipment(shipment_id)
    return [FieldCarryForwardResponse.model_validate(row) for row in rows]


@router.post(
    "",
    response_model=list[FieldCarryForwardResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_field_carry_forwards(
    body: FieldCarryForwardCreate,
    _authz: None = Depends(require_permission("can_manage_shipments", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> list[FieldCarryForwardResponse]:
    shipment = await ShipmentService(session).get_shipment(body.shipment_id)
    if shipment.quotation_id != body.quotation_id:
        raise InvalidFieldCarryForward("zlecenie nie należy do tej wyceny")
    rows = await FieldCarryForwardService(session).record_fields(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        quotation_id=body.quotation_id,
        shipment_id=shipment.id,
        fields=body.fields,
    )
    await session.commit()
    return [FieldCarryForwardResponse.model_validate(row) for row in rows]
