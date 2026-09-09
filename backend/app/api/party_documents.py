from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.party_document import PartyDocument
from app.services.parties.party_service import PartyService
from app.services.party_documents.party_document_service import PartyDocumentService

router = APIRouter(prefix="/party-documents", tags=["party-documents"])

_PERM = "can_manage_party_documents"


class PartyDocumentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    party_id: UUID
    document_kind: str
    source_ref: str


class PartyDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    party_id: UUID
    document_kind: str
    source_ref: str


def _as_row(row: PartyDocument) -> PartyDocumentResponse:
    return PartyDocumentResponse(
        id=row.id,
        organization_id=row.organization_id,
        party_id=row.party_id,
        document_kind=row.document_kind,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[PartyDocumentResponse])
async def list_party_documents(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PartyDocumentResponse]:
    rows = await PartyDocumentService(session).list_documents()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=PartyDocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_party_document(
    body: PartyDocumentCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PartyDocumentResponse:
    party = await PartyService(session).get_party(body.party_id)
    row = await PartyDocumentService(session).persist_document(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=party.id,
        document_kind=body.document_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
