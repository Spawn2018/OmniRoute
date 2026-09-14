from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.product_ticket_mark import ProductTicketMark
from app.services.product_ticket_marks.product_ticket_mark_service import (
    ProductTicketMarkService,
)

router = APIRouter(
    prefix="/product-ticket-marks",
    tags=["product-ticket-marks"],
)

_PERM = "can_manage_product_ticket_marks"


class ProductTicketMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    ticket_kind: str
    source_ref: str


class ProductTicketMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    ticket_kind: str
    source_ref: str


def _row(saved: ProductTicketMark) -> ProductTicketMarkResponse:
    return ProductTicketMarkResponse.model_validate(saved)


@router.get("", response_model=list[ProductTicketMarkResponse])
async def list_product_ticket_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ProductTicketMarkResponse]:
    packed = await ProductTicketMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ProductTicketMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product_ticket_mark(
    body: ProductTicketMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ProductTicketMarkResponse:
    saved = await ProductTicketMarkService(session).persist_product_ticket_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        ticket_kind=body.ticket_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
