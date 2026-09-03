from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.errors import InvalidMailDraft
from app.domain.mail_draft import mail_draft_mailto_href
from app.services.mail_drafts.mail_draft_service import MailDraftService
from app.services.operator_decisions.operator_decision_service import OperatorDecisionService
from app.services.parties.party_service import PartyService

router = APIRouter(prefix="/mail-drafts", tags=["mail-drafts"])

_AUTHZ = require_permission("can_manage_mail_drafts", "organization")


class MailDraftCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject_id: UUID
    body: str
    source_ref: str


class MailDraftDispatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    to_address: str = Field(min_length=1, max_length=320)
    party_id: UUID | None = None


class MailDraftResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    subject_kind: str
    subject_id: UUID
    body: str
    status: str
    to_address: str | None
    source_ref: str


class MailDraftDispatchResponse(BaseModel):
    id: UUID
    status: str
    to_address: str
    mailto: str
    blocks_auto: bool | None


@router.get("", response_model=list[MailDraftResponse])
async def list_mail_drafts(
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[MailDraftResponse]:
    rows = await MailDraftService(session).list_drafts()
    return [MailDraftResponse.model_validate(row) for row in rows]


@router.post("", response_model=MailDraftResponse, status_code=status.HTTP_201_CREATED)
async def create_mail_draft(
    body: MailDraftCreate,
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> MailDraftResponse:
    row = await MailDraftService(session).create_draft(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        subject_id=body.subject_id,
        body=body.body,
        source_ref=body.source_ref,
    )
    await session.commit()
    return MailDraftResponse.model_validate(row)


@router.post("/{draft_id}/dispatch-mailto", response_model=MailDraftDispatchResponse)
async def dispatch_mail_draft_mailto(
    draft_id: UUID,
    body: MailDraftDispatch,
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
) -> MailDraftDispatchResponse:
    drafts = MailDraftService(session)
    row = await drafts.get_draft(draft_id)
    accepted = await OperatorDecisionService(session).has_accepted("mail_draft", row.id)
    if not accepted:
        raise InvalidMailDraft("szkic bez akceptacji")
    blocks_auto: bool | None = None
    if body.party_id is not None:
        blocks_auto = await PartyService(session).party_blocks_auto(body.party_id)
    sent = await drafts.mark_sent(row.id, body.to_address)
    await session.commit()
    address = sent.to_address
    if address is None:
        raise InvalidMailDraft("adres jest obowiązkowy")
    return MailDraftDispatchResponse(
        id=sent.id,
        status=sent.status,
        to_address=address,
        mailto=mail_draft_mailto_href(address, sent.body),
        blocks_auto=blocks_auto,
    )
