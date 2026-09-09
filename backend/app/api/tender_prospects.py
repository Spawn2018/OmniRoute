from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_prospect import TenderProspect
from app.services.parties.party_service import PartyService
from app.services.tender_prospects.tender_prospect_service import TenderProspectService
from app.services.tenders.tender_service import TenderService

router = APIRouter(prefix="/tender-prospects", tags=["tender-prospects"])

_PERM = "can_manage_tender_prospects"


class TenderProspectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tender_id: UUID
    party_id: UUID
    outreach_code: str
    source_ref: str


class TenderProspectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    tender_id: UUID
    party_id: UUID
    outreach_code: str
    source_ref: str


def _as_row(row: TenderProspect) -> TenderProspectResponse:
    return TenderProspectResponse(
        id=row.id,
        organization_id=row.organization_id,
        tender_id=row.tender_id,
        party_id=row.party_id,
        outreach_code=row.outreach_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderProspectResponse])
async def list_tender_prospects(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderProspectResponse]:
    rows = await TenderProspectService(session).list_prospects()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=TenderProspectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tender_prospect(
    body: TenderProspectCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderProspectResponse:
    board = await TenderService(session).get_board(body.tender_id)
    party = await PartyService(session).get_party(body.party_id)
    row = await TenderProspectService(session).persist_prospect(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        tender_id=board.id,
        party_id=party.id,
        outreach_code=body.outreach_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
