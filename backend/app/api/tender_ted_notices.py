from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_ted_notice import TenderTedNotice
from app.services.tender_ted_notices.tender_ted_notice_service import (
    TenderTedNoticeService,
)
from app.services.tenders.tender_service import TenderService

router = APIRouter(prefix="/tender-ted-notices", tags=["tender-ted-notices"])

_PERM = "can_manage_tender_ted_notices"


class TenderTedNoticeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tender_id: UUID
    notice_number: str
    source_ref: str


class TenderTedNoticeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    tender_id: UUID
    notice_number: str
    source_ref: str


def _as_row(row: TenderTedNotice) -> TenderTedNoticeResponse:
    return TenderTedNoticeResponse(
        id=row.id,
        organization_id=row.organization_id,
        tender_id=row.tender_id,
        notice_number=row.notice_number,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderTedNoticeResponse])
async def list_tender_ted_notices(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderTedNoticeResponse]:
    rows = await TenderTedNoticeService(session).list_notices()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=TenderTedNoticeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tender_ted_notice(
    body: TenderTedNoticeCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderTedNoticeResponse:
    board = await TenderService(session).get_board(body.tender_id)
    row = await TenderTedNoticeService(session).persist_notice(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        tender_id=board.id,
        notice_number=body.notice_number,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
