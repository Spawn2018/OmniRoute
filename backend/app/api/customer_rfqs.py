from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.customer_rfqs.customer_rfq_service import CustomerRfqService
from app.services.inbound_messages.inbound_message_service import InboundMessageService

router = APIRouter(prefix="/customer-rfqs", tags=["customer-rfqs"])


class CustomerRfqCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    inbound_message_id: UUID


class CustomerRfqResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    inbound_message_id: UUID
    source_ref: str
    status: str
    party_id: UUID | None


@router.get("", response_model=list[CustomerRfqResponse])
async def list_customer_rfqs(
    _authz: None = Depends(require_permission("can_manage_customer_rfqs", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CustomerRfqResponse]:
    rows = await CustomerRfqService(session).list_rfqs()
    return [CustomerRfqResponse.model_validate(row) for row in rows]


@router.post("", response_model=CustomerRfqResponse, status_code=status.HTTP_201_CREATED)
async def create_customer_rfq(
    body: CustomerRfqCreate,
    _authz: None = Depends(require_permission("can_manage_customer_rfqs", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CustomerRfqResponse:
    message = await InboundMessageService(session).get_message(body.inbound_message_id)
    row = await CustomerRfqService(session).create_rfq(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        inbound_message_id=message.id,
        source_ref=message.source_ref,
        party_id=message.party_id,
    )
    await session.commit()
    return CustomerRfqResponse.model_validate(row)
