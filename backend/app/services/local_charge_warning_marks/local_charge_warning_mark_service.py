from typing import NoReturn
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import LocalChargeWarningMarkConflict
from app.domain.local_charge_warning_mark import parse_local_charge_warning_mark_row
from app.models.local_charge_warning_mark import LocalChargeWarningMark
from app.repositories.local_charge_warning_marks.local_charge_warning_mark_repository import (
    LocalChargeWarningMarkRepository,
)


def _raise_create_conflict(orig: IntegrityError) -> NoReturn:
    detail = str(orig.orig) if orig.orig is not None else str(orig)
    if "uq_local_charge_warning_mark_org_code" in detail:
        raise LocalChargeWarningMarkConflict(
            "ten kod ostrzeżenia dopłaty już istnieje",
        ) from orig
    if "uq_local_charge_warning_mark_org_source_ref" in detail:
        raise LocalChargeWarningMarkConflict(
            "to wskazanie ostrzeżenia dopłaty już istnieje",
        ) from orig
    raise orig


class LocalChargeWarningMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = LocalChargeWarningMarkRepository(session)

    async def list_marks(self) -> list[LocalChargeWarningMark]:
        return await self._repo.list_marks()

    async def persist_local_charge_warning_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        warning_kind: object,
        source_ref: object,
    ) -> LocalChargeWarningMark:
        code, kind, origin = parse_local_charge_warning_mark_row(
            mark_code,
            warning_kind,
            source_ref,
        )
        row = LocalChargeWarningMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            warning_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        try:
            return await self._repo.add_mark(row)
        except IntegrityError as exc:
            _raise_create_conflict(exc)
