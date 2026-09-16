from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.inbound_message import (
    inbound_extract_text,
    require_graph_source_ref,
    require_mailbox_source_ref,
)
from app.services.extraction.extraction_service import ExtractionService
from app.services.inbound_messages.inbound_message_service import InboundMessageService
from app.services.outbox_events.outbox_event_service import OutboxEventService
from app.services.parties.party_service import PartyService

router = APIRouter(prefix="/inbound-messages", tags=["inbound-messages"])


class InboundMessageCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_ref: str = Field(min_length=1, max_length=512)
    from_address: str = Field(min_length=1, max_length=320)
    subject: str = Field(min_length=1, max_length=512)
    body_text: str = Field(min_length=1, max_length=65536)
    rfc822_message_id: str | None = Field(default=None, max_length=512)
    in_reply_to: str | None = Field(default=None, max_length=512)


class InboundGraphIngest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    external_id: str = Field(min_length=1, max_length=256)
    source_ref: str = Field(min_length=1, max_length=512)
    from_address: str = Field(min_length=1, max_length=320)
    subject: str = Field(min_length=1, max_length=512)
    body_text: str = Field(min_length=1, max_length=65536)


class InboundMailboxIngest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    external_id: str = Field(min_length=1, max_length=256)
    source_ref: str = Field(min_length=1, max_length=512)
    from_address: str = Field(min_length=1, max_length=320)
    subject: str = Field(min_length=1, max_length=512)
    body_text: str = Field(min_length=1, max_length=65536)


class InboundMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    source_ref: str
    from_address: str
    subject: str
    body_text: str
    status: str
    party_id: UUID | None
    external_id: str | None
    rfc822_message_id: str | None
    in_reply_to: str | None


class InboundExtractResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    source_ref: str


@router.get("", response_model=list[InboundMessageResponse])
async def list_inbound_messages(
    _authz: None = Depends(require_permission("can_manage_inbound_messages", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[InboundMessageResponse]:
    service = InboundMessageService(session)
    rows = await service.list_messages()
    return [InboundMessageResponse.model_validate(row) for row in rows]


@router.post("", response_model=InboundMessageResponse, status_code=status.HTTP_201_CREATED)
async def create_inbound_message(
    body: InboundMessageCreate,
    _authz: None = Depends(require_permission("can_manage_inbound_messages", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> InboundMessageResponse:
    service = InboundMessageService(session)
    row = await service.create_message(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        source_ref=body.source_ref,
        from_address=body.from_address,
        subject=body.subject,
        body_text=body.body_text,
        rfc822_message_id=body.rfc822_message_id,
        in_reply_to=body.in_reply_to,
    )
    await OutboxEventService(session).record_message_saved(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        subject_id=row.id,
        source_ref=f"outbox://inbound-message/{row.id}",
    )
    await session.commit()
    return InboundMessageResponse.model_validate(row)


@router.post("/ingest-graph", response_model=InboundMessageResponse)
async def ingest_graph_inbound_message(
    body: InboundGraphIngest,
    _authz: None = Depends(require_permission("can_manage_inbound_messages", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> InboundMessageResponse:
    row = await InboundMessageService(session).ingest_by_external_id(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        external_id=body.external_id,
        source_ref=body.source_ref,
        from_address=body.from_address,
        subject=body.subject,
        body_text=body.body_text,
        require_origin=require_graph_source_ref,
    )
    await OutboxEventService(session).record_message_saved(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        subject_id=row.id,
        source_ref=f"outbox://inbound-message/{row.id}",
    )
    await session.commit()
    return InboundMessageResponse.model_validate(row)


@router.post("/ingest-imap", response_model=InboundMessageResponse)
async def ingest_mailbox_inbound_message(
    body: InboundMailboxIngest,
    _authz: None = Depends(require_permission("can_manage_inbound_messages", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> InboundMessageResponse:
    row = await InboundMessageService(session).ingest_by_external_id(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        external_id=body.external_id,
        source_ref=body.source_ref,
        from_address=body.from_address,
        subject=body.subject,
        body_text=body.body_text,
        require_origin=require_mailbox_source_ref,
    )
    await OutboxEventService(session).record_message_saved(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        subject_id=row.id,
        source_ref=f"outbox://inbound-message/{row.id}",
    )
    await session.commit()
    return InboundMessageResponse.model_validate(row)


@router.post("/{message_id}/resolve-email", response_model=InboundMessageResponse)
async def resolve_inbound_message_email(
    message_id: UUID,
    _authz: None = Depends(require_permission("can_manage_inbound_messages", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> InboundMessageResponse:
    messages = InboundMessageService(session)
    row = await messages.get_message(message_id)
    party = await PartyService(session).resolve_email(row.from_address)
    attached = await messages.attach_party(row.id, party.id)
    await session.commit()
    return InboundMessageResponse.model_validate(attached)


@router.post(
    "/{message_id}/extract",
    response_model=InboundExtractResponse,
    status_code=status.HTTP_201_CREATED,
)
async def extract_inbound_message(
    message_id: UUID,
    _authz: None = Depends(require_permission("can_manage_inbound_messages", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> InboundExtractResponse:
    row = await InboundMessageService(session).get_message(message_id)
    draft = await ExtractionService(session).extract_to_draft(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        source_ref=row.source_ref,
        input_text=inbound_extract_text(row.subject, row.body_text),
    )
    await session.commit()
    return InboundExtractResponse(
        id=draft.id,
        status=draft.status,
        source_ref=draft.source_ref,
    )
