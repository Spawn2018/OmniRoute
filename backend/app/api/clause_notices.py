from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.clause_notice import ClauseNotice
from app.services.clause_notices.clause_notice_service import ClauseNoticeService

router = APIRouter(prefix="/clause-notices", tags=["clause-notices"])

_PERM = "can_manage_clause_notices"


class ClauseNoticeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    notice_code: str
    clause_label: str
    source_ref: str


class ClauseNoticeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    notice_code: str
    clause_label: str
    source_ref: str


def _row(saved: ClauseNotice) -> ClauseNoticeResponse:
    return ClauseNoticeResponse.model_validate(saved)


@router.get("", response_model=list[ClauseNoticeResponse])
async def list_clause_notices(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ClauseNoticeResponse]:
    packed = await ClauseNoticeService(session).list_notices()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ClauseNoticeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_clause_notice(
    body: ClauseNoticeCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ClauseNoticeResponse:
    saved = await ClauseNoticeService(session).persist_clause_notice(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        notice_code=body.notice_code,
        clause_label=body.clause_label,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
