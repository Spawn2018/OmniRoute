from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_playbook import TenderPlaybook
from app.services.tender_playbooks.tender_playbook_service import TenderPlaybookService
from app.services.tenders.tender_service import TenderService

router = APIRouter(prefix="/tender-playbooks", tags=["tender-playbooks"])

_PERM = "can_manage_tender_playbooks"


class TenderPlaybookCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tender_id: UUID
    claim_code: str
    claim_text: str
    source_ref: str


class TenderPlaybookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    tender_id: UUID
    claim_code: str
    claim_text: str
    source_ref: str


def _as_row(row: TenderPlaybook) -> TenderPlaybookResponse:
    return TenderPlaybookResponse(
        id=row.id,
        organization_id=row.organization_id,
        tender_id=row.tender_id,
        claim_code=row.claim_code,
        claim_text=row.claim_text,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderPlaybookResponse])
async def list_tender_playbooks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderPlaybookResponse]:
    rows = await TenderPlaybookService(session).list_plays()
    return [_as_row(row) for row in rows]


@router.post("", response_model=TenderPlaybookResponse, status_code=status.HTTP_201_CREATED)
async def create_tender_playbook(
    body: TenderPlaybookCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderPlaybookResponse:
    board = await TenderService(session).get_board(body.tender_id)
    row = await TenderPlaybookService(session).record_play(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        tender_id=board.id,
        claim_code=body.claim_code,
        claim_text=body.claim_text,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
