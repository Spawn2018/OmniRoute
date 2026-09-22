from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.pallet_ledger import PalletLedger
from app.services.pallet_ledgers.pallet_ledger_service import PalletLedgerService
from app.services.parties.party_service import PartyService

router = APIRouter(prefix="/pallet-ledgers", tags=["pallet-ledgers"])

_PERM = "can_manage_pallet_ledgers"


class PalletLedgerCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    party_id: UUID
    movement_code: str
    pallet_kind: str
    delta_count: int
    source_ref: str


class PalletLedgerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    party_id: UUID
    movement_code: str
    pallet_kind: str
    delta_count: int
    source_ref: str


def _as_row(row: PalletLedger) -> PalletLedgerResponse:
    return PalletLedgerResponse.model_validate(row)


@router.get("", response_model=list[PalletLedgerResponse])
async def list_pallet_ledgers(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PalletLedgerResponse]:
    rows = await PalletLedgerService(session).list_movements()
    return [_as_row(row) for row in rows]


@router.post("", response_model=PalletLedgerResponse, status_code=status.HTTP_201_CREATED)
async def create_pallet_ledger(
    body: PalletLedgerCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PalletLedgerResponse:
    counterpart = await PartyService(session).get_party(body.party_id)
    row = await PalletLedgerService(session).record_movement(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=counterpart.id,
        movement_code=body.movement_code,
        pallet_kind=body.pallet_kind,
        delta_count=body.delta_count,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
