from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.document_kind_match_mark import DocumentKindMatchMark
from app.services.document_kind_match_marks.document_kind_match_mark_service import (
    DocumentKindMatchMarkService,
)

router = APIRouter(
    prefix="/document-kind-match-marks",
    tags=["document-kind-match-marks"],
)

_PERM = "can_manage_document_kind_match_marks"


class DocumentKindMatchMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    match_kind: str
    source_ref: str


class DocumentKindMatchMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    match_kind: str
    source_ref: str


def _row(saved: DocumentKindMatchMark) -> DocumentKindMatchMarkResponse:
    return DocumentKindMatchMarkResponse.model_validate(saved)


@router.get("", response_model=list[DocumentKindMatchMarkResponse])
async def list_document_kind_match_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[DocumentKindMatchMarkResponse]:
    packed = await DocumentKindMatchMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=DocumentKindMatchMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_document_kind_match_mark(
    body: DocumentKindMatchMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> DocumentKindMatchMarkResponse:
    saved = await DocumentKindMatchMarkService(session).persist_document_kind_match_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        match_kind=body.match_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
