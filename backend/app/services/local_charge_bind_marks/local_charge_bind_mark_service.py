from typing import NoReturn
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import LocalChargeBindMarkConflict
from app.domain.local_charge_bind_mark import parse_local_charge_bind_mark_row
from app.models.local_charge_bind_mark import LocalChargeBindMark
from app.repositories.local_charge_bind_marks.local_charge_bind_mark_repository import (
    LocalChargeBindMarkRepository,
)


def _raise_create_conflict(orig: IntegrityError) -> NoReturn:
    detail = str(orig.orig) if orig.orig is not None else str(orig)
    if "uq_local_charge_bind_mark_org_code" in detail:
        raise LocalChargeBindMarkConflict(
            "ten kod wiązania dopłaty lokalnej już istnieje",
        ) from orig
    if "uq_local_charge_bind_mark_org_source_ref" in detail:
        raise LocalChargeBindMarkConflict(
            "to wskazanie wiązania dopłaty lokalnej już istnieje",
        ) from orig
    raise orig


class LocalChargeBindMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = LocalChargeBindMarkRepository(session)

    async def list_marks(self) -> list[LocalChargeBindMark]:
        return await self._repo.list_marks()

    async def persist_local_charge_bind_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        bind_kind: object,
        source_ref: object,
    ) -> LocalChargeBindMark:
        code, kind, origin = parse_local_charge_bind_mark_row(
            mark_code,
            bind_kind,
            source_ref,
        )
        row = LocalChargeBindMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            bind_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        try:
            return await self._repo.add_mark(row)
        except IntegrityError as exc:
            _raise_create_conflict(exc)
