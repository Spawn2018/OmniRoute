from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.document_template import DocumentTemplate
from app.services.document_templates.document_template_service import (
    DocumentTemplateService,
)

router = APIRouter(prefix="/document-templates", tags=["document-templates"])

_PERM = "can_manage_document_templates"


class DocumentTemplateCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    template_kind: str
    language: str
    layout_ref: str
    output_kind: str
    source_ref: str


class DocumentTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    template_kind: str
    language: str
    layout_ref: str
    output_kind: str
    source_ref: str


def _as_row(row: DocumentTemplate) -> DocumentTemplateResponse:
    return DocumentTemplateResponse.model_validate(row)


@router.get("", response_model=list[DocumentTemplateResponse])
async def list_document_templates(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[DocumentTemplateResponse]:
    rows = await DocumentTemplateService(session).list_templates()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=DocumentTemplateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_document_template(
    body: DocumentTemplateCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> DocumentTemplateResponse:
    row = await DocumentTemplateService(session).record_template(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        template_kind=body.template_kind,
        language=body.language,
        layout_ref=body.layout_ref,
        output_kind=body.output_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
