from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.relation_document_requirement import RelationDocumentRequirement
from app.services.relation_document_requirements.relation_document_requirement_service import (
    RelationDocumentRequirementService,
)

router = APIRouter(
    prefix="/relation-document-requirements",
    tags=["relation-document-requirements"],
)

_PERM = "can_manage_relation_document_requirements"


class RelationDocumentRequirementCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requirement_code: str
    relation_kind: str
    source_ref: str


class RelationDocumentRequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    requirement_code: str
    relation_kind: str
    source_ref: str


def _row(saved: RelationDocumentRequirement) -> RelationDocumentRequirementResponse:
    return RelationDocumentRequirementResponse.model_validate(saved)


@router.get("", response_model=list[RelationDocumentRequirementResponse])
async def list_relation_document_requirements(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RelationDocumentRequirementResponse]:
    packed = await RelationDocumentRequirementService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=RelationDocumentRequirementResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_relation_document_requirement(
    body: RelationDocumentRequirementCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RelationDocumentRequirementResponse:
    saved = await RelationDocumentRequirementService(session).persist_relation_document_requirement(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        requirement_code=body.requirement_code,
        relation_kind=body.relation_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
