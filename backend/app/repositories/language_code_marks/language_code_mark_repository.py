from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.language_code_mark import LanguageCodeMark


def _language_code_catalog_query() -> Select[tuple[LanguageCodeMark]]:
    return select(LanguageCodeMark).order_by(
        LanguageCodeMark.mark_code.asc(),
        LanguageCodeMark.created_at.desc(),
    )


class LanguageCodeMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[LanguageCodeMark]:
        loaded = await self._session.scalars(_language_code_catalog_query())
        batch: Sequence[LanguageCodeMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: LanguageCodeMark) -> LanguageCodeMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
