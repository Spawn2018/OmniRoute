from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.edi_messages.edi_message_service import EdiMessageService
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/edi-messages", tags=["edi-messages"])


class EdiMessageCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    message_kind: str
    source_ref: str


class EdiMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    message_kind: str
    source_ref: str


@router.get("", response_model=list[EdiMessageResponse])
async def list_edi_messages(
    _authz: None = Depends(require_permission("can_manage_edi_messages", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[EdiMessageResponse]:
    rows = await EdiMessageService(session).list_messages()
    return [EdiMessageResponse.model_validate(row) for row in rows]


@router.post(
    "",
    response_model=EdiMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_edi_message(
    body: EdiMessageCreate,
    _authz: None = Depends(require_permission("can_manage_edi_messages", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> EdiMessageResponse:
    shipment = await ShipmentService(session).get_shipment(body.shipment_id)
    row = await EdiMessageService(session).record_message(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=shipment.id,
        message_kind=body.message_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return EdiMessageResponse.model_validate(row)
