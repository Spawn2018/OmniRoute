"""HTTP katalog referencji PO klienta — HITL, bez purchase_order CT1 i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.customer_po_mark import CustomerPoMark
from app.services.customer_po_marks.customer_po_mark_service import (
    CustomerPoMarkService,
)

router = APIRouter(prefix="/customer-po-marks", tags=["customer-po-mark"])
_PERM = "can_manage_customer_po_marks"


class CustomerPoMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    ref_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class CustomerPoMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    ref_kind: str
    source_ref: str


def _to_dto(row: CustomerPoMark) -> CustomerPoMarkResponse:
    return CustomerPoMarkResponse.model_validate(row)


@router.get("", response_model=list[CustomerPoMarkResponse])
async def list_customer_po_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CustomerPoMarkResponse]:
    catalog = CustomerPoMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=CustomerPoMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer_po_mark(
    body: CustomerPoMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CustomerPoMarkResponse:
    catalog = CustomerPoMarkService(session)
    saved = await catalog.persist_customer_po_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        ref_kind=body.ref_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "customer-po-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
