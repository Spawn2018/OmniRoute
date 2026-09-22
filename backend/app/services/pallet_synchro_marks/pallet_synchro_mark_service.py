from typing import NoReturn
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import PalletSynchroMarkConflict
from app.domain.pallet_synchro_mark import parse_pallet_synchro_mark_row
from app.models.pallet_synchro_mark import PalletSynchroMark
from app.repositories.pallet_synchro_marks.pallet_synchro_mark_repository import (
    PalletSynchroMarkRepository,
)


def _raise_create_conflict(orig: IntegrityError) -> NoReturn:
    detail = str(orig.orig) if orig.orig is not None else str(orig)
    if "uq_pallet_synchro_mark_org_code" in detail:
        raise PalletSynchroMarkConflict("ten kod synchro palet już istnieje") from orig
    if "uq_pallet_synchro_mark_org_source_ref" in detail:
        raise PalletSynchroMarkConflict("to wskazanie synchro palet już istnieje") from orig
    raise orig


class PalletSynchroMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = PalletSynchroMarkRepository(session)

    async def list_marks(self) -> list[PalletSynchroMark]:
        return await self._repo.list_marks()

    async def persist_pallet_synchro_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        synchro_kind: object,
        source_ref: object,
    ) -> PalletSynchroMark:
        code, kind, origin = parse_pallet_synchro_mark_row(
            mark_code,
            synchro_kind,
            source_ref,
        )
        row = PalletSynchroMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            synchro_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        try:
            return await self._repo.add_mark(row)
        except IntegrityError as exc:
            _raise_create_conflict(exc)
