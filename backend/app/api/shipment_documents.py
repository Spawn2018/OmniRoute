from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.shipment_documents.shipment_document_service import ShipmentDocumentService
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/shipment-documents", tags=["shipment-documents"])


class ShipmentDocumentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    document_kind: str
    source_ref: str


class ShipmentDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    document_kind: str
    source_ref: str


@router.get("", response_model=list[ShipmentDocumentResponse])
async def list_shipment_documents(
    _authz: None = Depends(require_permission("can_manage_shipment_documents", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ShipmentDocumentResponse]:
    rows = await ShipmentDocumentService(session).list_documents()
    return [ShipmentDocumentResponse.model_validate(row) for row in rows]


@router.post("", response_model=ShipmentDocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment_document(
    body: ShipmentDocumentCreate,
    _authz: None = Depends(require_permission("can_manage_shipment_documents", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipmentDocumentResponse:
    shipment = await ShipmentService(session).get_shipment(body.shipment_id)
    row = await ShipmentDocumentService(session).record_document(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=shipment.id,
        document_kind=body.document_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return ShipmentDocumentResponse.model_validate(row)
