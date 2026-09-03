from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.shipment import require_party_on_quotation
from app.services.quotations.quotation_service import QuotationService
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/shipments", tags=["shipments"])


class ShipmentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quotation_id: UUID
    source_ref: str


class ShipmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    quotation_id: UUID
    party_id: UUID
    source_ref: str
    status: str


@router.get("", response_model=list[ShipmentResponse])
async def list_shipments(
    _authz: None = Depends(require_permission("can_manage_shipments", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ShipmentResponse]:
    rows = await ShipmentService(session).list_shipments()
    return [ShipmentResponse.model_validate(row) for row in rows]


@router.post("", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment(
    body: ShipmentCreate,
    _authz: None = Depends(require_permission("can_manage_shipments", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipmentResponse:
    quote = await QuotationService(session).get_quotation(body.quotation_id)
    row = await ShipmentService(session).create_shipment(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        quotation_id=quote.id,
        party_id=require_party_on_quotation(quote.party_id),
        source_ref=body.source_ref,
    )
    await session.commit()
    return ShipmentResponse.model_validate(row)
