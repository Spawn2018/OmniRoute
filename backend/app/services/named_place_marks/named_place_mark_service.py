from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.named_place_mark import parse_named_place_mark_row
from app.models.named_place_mark import NamedPlaceMark
from app.repositories.named_place_marks.named_place_mark_repository import (
    NamedPlaceMarkRepository,
)


class NamedPlaceMarkService:
    """HITL katalog miejsca nazwanego — bez cytatu ICC i bez mutacji wyceny."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = NamedPlaceMarkRepository(session)

    async def list_marks(self) -> list[NamedPlaceMark]:
        return await self._marks.list_marks()

    async def persist_named_place_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        named_place: object,
        terms_version: object,
        source_ref: object,
    ) -> NamedPlaceMark:
        code, place, version, pointer = parse_named_place_mark_row(
            mark_code,
            named_place,
            terms_version,
            source_ref,
        )
        row = NamedPlaceMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            named_place=place,
            terms_version=version,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
