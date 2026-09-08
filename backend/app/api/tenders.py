from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender import Tender
from app.services.parties.party_service import PartyService
from app.services.tenders.tender_service import TenderService

router = APIRouter(prefix="/tenders", tags=["tenders"])

_PERM = "can_manage_tenders"


class TenderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    side: str
    kind: str
    status: str
    buyer_party_id: UUID
    deadline_at: str
    incoterm: str
    trade_side: str
    named_place: str
    source_ref: str


class TenderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    side: str
    kind: str
    status: str
    buyer_party_id: UUID
    deadline_at: str
    incoterm: str
    trade_side: str
    named_place: str
    source_ref: str


def _as_row(row: Tender) -> TenderResponse:
    return TenderResponse(
        id=row.id,
        organization_id=row.organization_id,
        side=row.side,
        kind=row.kind,
        status=row.status,
        buyer_party_id=row.buyer_party_id,
        deadline_at=row.deadline_at.isoformat(),
        incoterm=row.incoterm,
        trade_side=row.trade_side,
        named_place=row.named_place,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderResponse])
async def list_tenders(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderResponse]:
    rows = await TenderService(session).list_boards()
    return [_as_row(row) for row in rows]


@router.post("", response_model=TenderResponse, status_code=status.HTTP_201_CREATED)
async def create_tender(
    body: TenderCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderResponse:
    buyer = await PartyService(session).get_party(body.buyer_party_id)
    row = await TenderService(session).record_board(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        side=body.side,
        kind=body.kind,
        status=body.status,
        buyer_party_id=buyer.id,
        deadline_at=body.deadline_at,
        incoterm=body.incoterm,
        trade_side=body.trade_side,
        named_place=body.named_place,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
