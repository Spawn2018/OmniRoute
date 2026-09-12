"""HTTP katalog Terms AI — HITL, bez live mapa/GPS."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.mail_accept_mark import MailAcceptMark
from app.services.mail_accept_marks.mail_accept_mark_service import MailAcceptMarkService

router = APIRouter(prefix="/mail-accept-marks", tags=["funnel"])

_PERM = "can_manage_mail_accept_marks"

class MailAcceptMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    accept_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)

class MailAcceptMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    accept_kind: str
    source_ref: str

def _to_dto(row: MailAcceptMark) -> MailAcceptMarkResponse:
    return MailAcceptMarkResponse.model_validate(row)

@router.get("", response_model=list[MailAcceptMarkResponse])
async def list_mail_accept_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[MailAcceptMarkResponse]:
    catalog = MailAcceptMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]

@router.post("", response_model=MailAcceptMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_mail_accept_mark(
    body: MailAcceptMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> MailAcceptMarkResponse:
    catalog = MailAcceptMarkService(session)
    saved = await catalog.persist_mail_accept_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        accept_kind=body.accept_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "mail-accept-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
