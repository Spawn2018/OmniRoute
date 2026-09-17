from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.errors import (
    InvalidOperatorDecision,
    InvalidProductTicket,
    OperatorDecisionConflict,
    ProductTicketOwnerRequired,
)
from app.models.operator_decision import OperatorDecision
from app.models.product_ticket import ProductTicket
from app.services.operator_decisions.operator_decision_service import (
    OperatorDecisionService,
)
from app.services.product_tickets.product_ticket_service import ProductTicketService

router = APIRouter(
    prefix="/product-tickets",
    tags=["product-tickets"],
)

_PERM = "can_manage_product_tickets"
_OWNER_KIND = "product_ticket"
_OWNER_OK = "owner_ok"


class ProductTicketCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_code: str
    title: str
    body: str
    ticket_kind: str
    source_ref: str
    reviewed_ticket_id: UUID | None = None
    owner_decision_id: UUID | None = None


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


def _forbid_owner_fields(body: ProductTicketCreate) -> None:
    if body.reviewed_ticket_id is not None or body.owner_decision_id is not None:
        raise InvalidProductTicket(
            "reviewed_ticket_id i owner_decision_id tylko przy owner_ok",
        )


async def _accepted_owner_override(
    decisions: OperatorDecisionService,
    *,
    decision_id: UUID,
    ticket_id: UUID,
) -> None:
    row = await decisions.get_decision(decision_id)
    if (
        row.subject_kind != _OWNER_KIND
        or row.subject_id != ticket_id
        or row.status != "accepted"
    ):
        raise InvalidOperatorDecision(
            "owner_decision_id musi być accepted dla tego ticketu",
        )


async def _pending_for_owner(
    decisions: OperatorDecisionService,
    *,
    organization_id: UUID,
    user_id: UUID,
    ticket_id: UUID,
    source_ref: str,
) -> OperatorDecision:
    try:
        return await decisions.create_decision(
            organization_id=organization_id,
            user_id=user_id,
            subject_kind=_OWNER_KIND,
            subject_id=ticket_id,
            source_ref=source_ref,
        )
    except OperatorDecisionConflict:
        existing = await decisions.get_pending(_OWNER_KIND, ticket_id)
        if existing is None:
            raise
        return existing


async def _enforce_owner_ok(
    session: AsyncSession,
    identity: SessionIdentity,
    body: ProductTicketCreate,
) -> None:
    if body.reviewed_ticket_id is None:
        raise InvalidProductTicket("owner_ok wymaga reviewed_ticket_id")
    tickets = ProductTicketService(session)
    await tickets.get_ticket(body.reviewed_ticket_id)
    decisions = OperatorDecisionService(session)
    if body.owner_decision_id is not None:
        await _accepted_owner_override(
            decisions,
            decision_id=body.owner_decision_id,
            ticket_id=body.reviewed_ticket_id,
        )
        return
    pending = await _pending_for_owner(
        decisions,
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        ticket_id=body.reviewed_ticket_id,
        source_ref=body.source_ref,
    )
    raise ProductTicketOwnerRequired(
        "owner_ok wymaga akceptacji właściciela (S11)",
        decision_id=pending.id,
    )


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
    if body.ticket_kind.strip().lower() == _OWNER_OK:
        await _enforce_owner_ok(session, identity, body)
    else:
        _forbid_owner_fields(body)
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
