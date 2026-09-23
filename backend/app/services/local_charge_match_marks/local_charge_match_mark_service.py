from typing import NoReturn
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import LocalChargeMatchMarkConflict
from app.domain.local_charge_match_mark import parse_local_charge_match_mark_row
from app.models.local_charge_match_mark import LocalChargeMatchMark
from app.repositories.local_charge_match_marks.local_charge_match_mark_repository import (
    LocalChargeMatchMarkRepository,
)


def _raise_create_conflict(orig: IntegrityError) -> NoReturn:
    detail = str(orig.orig) if orig.orig is not None else str(orig)
    if "uq_local_charge_match_mark_org_code" in detail:
        raise LocalChargeMatchMarkConflict(
            "ten kod dopasowania dopłaty lokalnej już istnieje",
        ) from orig
    if "uq_local_charge_match_mark_org_source_ref" in detail:
        raise LocalChargeMatchMarkConflict(
            "to wskazanie dopasowania dopłaty lokalnej już istnieje",
        ) from orig
    raise orig


class LocalChargeMatchMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = LocalChargeMatchMarkRepository(session)

    async def list_marks(self) -> list[LocalChargeMatchMark]:
        return await self._repo.list_marks()

    async def persist_local_charge_match_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        match_kind: object,
        source_ref: object,
    ) -> LocalChargeMatchMark:
        code, kind, origin = parse_local_charge_match_mark_row(
            mark_code,
            match_kind,
            source_ref,
        )
        row = LocalChargeMatchMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            match_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        try:
            return await self._repo.add_mark(row)
        except IntegrityError as exc:
            _raise_create_conflict(exc)
