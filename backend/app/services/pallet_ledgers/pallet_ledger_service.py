from typing import NoReturn
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import PalletLedgerConflict
from app.domain.pallet_ledger import (
    require_delta_count,
    require_ledger_pallet_kind,
    require_ledger_party_id,
    require_ledger_source_ref,
    require_movement_code,
)
from app.models.pallet_ledger import PalletLedger
from app.repositories.pallet_ledgers.pallet_ledger_repository import PalletLedgerRepository


def _raise_create_conflict(orig: IntegrityError) -> NoReturn:
    detail = str(orig.orig) if orig.orig is not None else str(orig)
    if "uq_pallet_ledger_org_code" in detail:
        raise PalletLedgerConflict("ten kod ruchu palet już istnieje") from orig
    if "fk_pallet_ledger_party" in detail:
        raise PalletLedgerConflict("kontrahent ruchu palet nie istnieje") from orig
    raise orig


class PalletLedgerService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PalletLedgerRepository(session)

    async def list_movements(self) -> list[PalletLedger]:
        return await self._rows.list_all()

    async def record_movement(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: object,
        movement_code: object,
        pallet_kind: object,
        delta_count: object,
        source_ref: object,
    ) -> PalletLedger:
        row = PalletLedger(
            id=uuid4(),
            organization_id=organization_id,
            party_id=require_ledger_party_id(party_id),
            movement_code=require_movement_code(movement_code),
            pallet_kind=require_ledger_pallet_kind(pallet_kind),
            delta_count=require_delta_count(delta_count),
            source_ref=require_ledger_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            _raise_create_conflict(orig)
