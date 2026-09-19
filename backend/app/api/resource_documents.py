from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.resource_document import ResourceDocument
from app.services.resource_documents.resource_document_service import ResourceDocumentService

router = APIRouter(prefix="/resource-documents", tags=["resource-documents"])

_SHIP = "can_manage_shipments"


class ResourceDocumentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    resource_id: UUID
    document_kind: str
    valid_until: str
    source_ref: str


class ResourceDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    resource_id: UUID
    document_kind: str
    valid_until: date
    source_ref: str


def _as_response(row: ResourceDocument) -> ResourceDocumentResponse:
    return ResourceDocumentResponse.model_validate(row)


@router.get("", response_model=list[ResourceDocumentResponse])
async def list_resource_documents(
    _authz: None = Depends(require_permission(_SHIP, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ResourceDocumentResponse]:
    rows = await ResourceDocumentService(session).list_documents()
    return [_as_response(row) for row in rows]


@router.post("", response_model=ResourceDocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_resource_document(
    body: ResourceDocumentCreate,
    _authz: None = Depends(require_permission(_SHIP, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ResourceDocumentResponse:
    row = await ResourceDocumentService(session).record_document(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        resource_id=body.resource_id,
        document_kind=body.document_kind,
        valid_until=body.valid_until,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(row)
