from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.mail_drafts.mail_draft_service import MailDraftService

router = APIRouter(prefix="/mail-drafts", tags=["mail-drafts"])

_AUTHZ = require_permission("can_manage_mail_drafts", "organization")


class MailDraftCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject_id: UUID
    body: str
    source_ref: str


class MailDraftResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    subject_kind: str
    subject_id: UUID
    body: str
    status: str
    source_ref: str


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
