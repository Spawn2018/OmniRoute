from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.invoice_alloc_mark import InvoiceAllocMark
from app.services.invoice_alloc_marks.invoice_alloc_mark_service import (
    InvoiceAllocMarkService,
)

router = APIRouter(prefix="/invoice-alloc-marks", tags=["invoice-alloc-marks"])

_PERM = "can_manage_invoice_alloc_marks"


class InvoiceAllocMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    alloc_kind: str
    source_ref: str


class InvoiceAllocMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    alloc_kind: str
    source_ref: str


def _row(saved: InvoiceAllocMark) -> InvoiceAllocMarkResponse:
    return InvoiceAllocMarkResponse.model_validate(saved)


@router.get("", response_model=list[InvoiceAllocMarkResponse])
async def list_invoice_alloc_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[InvoiceAllocMarkResponse]:
    packed = await InvoiceAllocMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=InvoiceAllocMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_invoice_alloc_mark(
    body: InvoiceAllocMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> InvoiceAllocMarkResponse:
    saved = await InvoiceAllocMarkService(session).persist_invoice_alloc_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        alloc_kind=body.alloc_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
