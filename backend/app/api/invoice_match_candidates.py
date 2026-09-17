from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.invoice_match_candidate import InvoiceMatchCandidate
from app.services.invoice_match_candidates.invoice_match_candidate_service import (
    InvoiceMatchCandidateService,
)

router = APIRouter(
    prefix="/invoice-match-candidates",
    tags=["invoice-match-candidates"],
)

_PERM = "can_manage_invoice_match_candidates"


class InvoiceMatchCandidateCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_code: str
    candidate_kind: str
    source_ref: str


class InvoiceMatchCandidateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    candidate_code: str
    candidate_kind: str
    source_ref: str


def _row(saved: InvoiceMatchCandidate) -> InvoiceMatchCandidateResponse:
    return InvoiceMatchCandidateResponse.model_validate(saved)


@router.get("", response_model=list[InvoiceMatchCandidateResponse])
async def list_invoice_match_candidates(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[InvoiceMatchCandidateResponse]:
    packed = await InvoiceMatchCandidateService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=InvoiceMatchCandidateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_invoice_match_candidate(
    body: InvoiceMatchCandidateCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> InvoiceMatchCandidateResponse:
    saved = await InvoiceMatchCandidateService(session).persist_invoice_match_candidate(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        candidate_code=body.candidate_code,
        candidate_kind=body.candidate_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
