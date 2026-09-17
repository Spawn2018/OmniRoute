from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.product_ticket import ProductTicket
from app.services.product_tickets.product_ticket_service import ProductTicketService

router = APIRouter(
    prefix="/product-tickets",
    tags=["product-tickets"],
)

_PERM = "can_manage_product_tickets"


class ProductTicketCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_code: str
    title: str
    body: str
    ticket_kind: str
    source_ref: str


class ProductTicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    ticket_code: str
    title: str
    body: str
    ticket_kind: str
    source_ref: str


def _row(saved: ProductTicket) -> ProductTicketResponse:
    return ProductTicketResponse.model_validate(saved)


@router.get("", response_model=list[ProductTicketResponse])
async def list_product_tickets(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ProductTicketResponse]:
    packed = await ProductTicketService(session).list_tickets()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ProductTicketResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product_ticket(
    body: ProductTicketCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ProductTicketResponse:
    saved = await ProductTicketService(session).persist_product_ticket(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        ticket_code=body.ticket_code,
        title=body.title,
        body=body.body,
        ticket_kind=body.ticket_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
