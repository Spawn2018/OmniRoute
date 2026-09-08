from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.pallet_balance import PalletBalance
from app.services.pallet_balances.pallet_balance_service import PalletBalanceService
from app.services.parties.party_service import PartyService

router = APIRouter(prefix="/pallet-balances", tags=["pallet-balances"])

_PERM = "can_manage_pallet_balances"


class PalletBalanceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    party_id: UUID
    pallet_kind: str
    unit_count: int
    source_ref: str


class PalletBalanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    party_id: UUID
    pallet_kind: str
    unit_count: int
    source_ref: str


def _as_row(row: PalletBalance) -> PalletBalanceResponse:
    return PalletBalanceResponse.model_validate(row)


@router.get("", response_model=list[PalletBalanceResponse])
async def list_pallet_balances(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PalletBalanceResponse]:
    rows = await PalletBalanceService(session).list_balances()
    return [_as_row(row) for row in rows]


@router.post("", response_model=PalletBalanceResponse, status_code=status.HTTP_201_CREATED)
async def create_pallet_balance(
    body: PalletBalanceCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PalletBalanceResponse:
    counterpart = await PartyService(session).get_party(body.party_id)
    row = await PalletBalanceService(session).record_balance(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=counterpart.id,
        pallet_kind=body.pallet_kind,
        unit_count=body.unit_count,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
