from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.suggestion_kind import SuggestionKind


def _kind_query() -> Select[tuple[SuggestionKind]]:
    return select(SuggestionKind).order_by(
        SuggestionKind.created_at.desc(),
        SuggestionKind.id,
    )


class SuggestionKindRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[SuggestionKind]:
        loaded = await self._session.scalars(_kind_query())
        batch: Sequence[SuggestionKind] = loaded.all()
        return list(batch)

    async def add(self, entity: SuggestionKind) -> SuggestionKind:
        self._session.add(entity)
        await self._session.flush()
        return entity
