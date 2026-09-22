from typing import NoReturn
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.clone_carry_mark import parse_clone_carry_mark_row
from app.domain.errors import CloneCarryMarkConflict
from app.models.clone_carry_mark import CloneCarryMark
from app.repositories.clone_carry_marks.clone_carry_mark_repository import (
    CloneCarryMarkRepository,
)


def _raise_create_conflict(orig: IntegrityError) -> NoReturn:
    detail = str(orig.orig) if orig.orig is not None else str(orig)
    if "uq_clone_carry_mark_org_code" in detail:
        raise CloneCarryMarkConflict("ten kod carry przy klonie już istnieje") from orig
    if "uq_clone_carry_mark_org_source_ref" in detail:
        raise CloneCarryMarkConflict(
            "to wskazanie carry przy klonie już istnieje",
        ) from orig
    raise orig


class CloneCarryMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = CloneCarryMarkRepository(session)

    async def list_marks(self) -> list[CloneCarryMark]:
        return await self._repo.list_marks()

    async def persist_clone_carry_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        carry_kind: object,
        source_ref: object,
    ) -> CloneCarryMark:
        code, kind, origin = parse_clone_carry_mark_row(
            mark_code,
            carry_kind,
            source_ref,
        )
        row = CloneCarryMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            carry_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        try:
            return await self._repo.add_mark(row)
        except IntegrityError as exc:
            _raise_create_conflict(exc)
