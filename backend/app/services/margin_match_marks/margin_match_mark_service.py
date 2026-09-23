from typing import NoReturn
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import MarginMatchMarkConflict
from app.domain.margin_match_mark import parse_margin_match_mark_row
from app.models.margin_match_mark import MarginMatchMark
from app.repositories.margin_match_marks.margin_match_mark_repository import (
    MarginMatchMarkRepository,
)


def _raise_create_conflict(orig: IntegrityError) -> NoReturn:
    detail = str(orig.orig) if orig.orig is not None else str(orig)
    if "uq_margin_match_mark_org_code" in detail:
        raise MarginMatchMarkConflict(
            "ten kod dopasowania podłogi już istnieje",
        ) from orig
    if "uq_margin_match_mark_org_source_ref" in detail:
        raise MarginMatchMarkConflict(
            "to wskazanie dopasowania podłogi już istnieje",
        ) from orig
    raise orig


class MarginMatchMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = MarginMatchMarkRepository(session)

    async def list_marks(self) -> list[MarginMatchMark]:
        return await self._repo.list_marks()

    async def persist_margin_match_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        match_kind: object,
        source_ref: object,
    ) -> MarginMatchMark:
        code, kind, origin = parse_margin_match_mark_row(
            mark_code,
            match_kind,
            source_ref,
        )
        row = MarginMatchMark(
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
