from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_consortium_member import TenderConsortiumMember
from app.services.parties.party_service import PartyService
from app.services.tender_consortium_members.tender_consortium_member_service import (
    TenderConsortiumMemberService,
)
from app.services.tenders.tender_service import TenderService

router = APIRouter(prefix="/tender-consortium-members", tags=["tender-consortium-members"])

_PERM = "can_manage_tender_consortium_members"


class TenderConsortiumMemberCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tender_id: UUID
    party_id: UUID
    seat_code: str
    source_ref: str


class TenderConsortiumMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    tender_id: UUID
    party_id: UUID
    seat_code: str
    source_ref: str


def _as_row(row: TenderConsortiumMember) -> TenderConsortiumMemberResponse:
    return TenderConsortiumMemberResponse(
        id=row.id,
        organization_id=row.organization_id,
        tender_id=row.tender_id,
        party_id=row.party_id,
        seat_code=row.seat_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderConsortiumMemberResponse])
async def list_tender_consortium_members(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderConsortiumMemberResponse]:
    rows = await TenderConsortiumMemberService(session).list_seats()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=TenderConsortiumMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tender_consortium_member(
    body: TenderConsortiumMemberCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderConsortiumMemberResponse:
    board = await TenderService(session).get_board(body.tender_id)
    party = await PartyService(session).get_party(body.party_id)
    row = await TenderConsortiumMemberService(session).persist_seat(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        tender_id=board.id,
        party_id=party.id,
        seat_code=body.seat_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
