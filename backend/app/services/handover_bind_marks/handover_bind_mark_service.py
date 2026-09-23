from typing import NoReturn
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import HandoverBindMarkConflict
from app.domain.handover_bind_mark import parse_handover_bind_mark_row
from app.models.handover_bind_mark import HandoverBindMark
from app.repositories.handover_bind_marks.handover_bind_mark_repository import (
    HandoverBindMarkRepository,
)


def _raise_create_conflict(orig: IntegrityError) -> NoReturn:
    detail = str(orig.orig) if orig.orig is not None else str(orig)
    if "uq_handover_bind_mark_org_code" in detail:
        raise HandoverBindMarkConflict(
            "ten kod wiązania przekazania już istnieje",
        ) from orig
    if "uq_handover_bind_mark_org_source_ref" in detail:
        raise HandoverBindMarkConflict(
            "to wskazanie wiązania przekazania już istnieje",
        ) from orig
    raise orig


class HandoverBindMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = HandoverBindMarkRepository(session)

    async def list_marks(self) -> list[HandoverBindMark]:
        return await self._repo.list_marks()

    async def persist_handover_bind_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        bind_kind: object,
        source_ref: object,
    ) -> HandoverBindMark:
        code, kind, origin = parse_handover_bind_mark_row(
            mark_code,
            bind_kind,
            source_ref,
        )
        row = HandoverBindMark(
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
