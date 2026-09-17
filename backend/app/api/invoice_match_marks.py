from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.invoice_match_mark import InvoiceMatchMark
from app.services.invoice_match_marks.invoice_match_mark_service import (
    InvoiceMatchMarkService,
)

router = APIRouter(prefix="/invoice-match-marks", tags=["invoice-match-marks"])

_PERM = "can_manage_invoice_match_marks"


class InvoiceMatchMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    match_kind: str
    source_ref: str


class InvoiceMatchMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    match_kind: str
    source_ref: str


def _row(saved: InvoiceMatchMark) -> InvoiceMatchMarkResponse:
    return InvoiceMatchMarkResponse.model_validate(saved)


@router.get("", response_model=list[InvoiceMatchMarkResponse])
async def list_invoice_match_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[InvoiceMatchMarkResponse]:
    packed = await InvoiceMatchMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=InvoiceMatchMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_invoice_match_mark(
    body: InvoiceMatchMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> InvoiceMatchMarkResponse:
    saved = await InvoiceMatchMarkService(session).persist_invoice_match_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        match_kind=body.match_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
