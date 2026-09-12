from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.terms_ai_mark import TermsAiMark


def _label_parking_catalog_query() -> Select[tuple[TermsAiMark]]:
    return select(TermsAiMark).order_by(
        TermsAiMark.mark_code.asc(),
        TermsAiMark.created_at.desc(),
    )

class TermsAiMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[TermsAiMark]:
        loaded = await self._session.scalars(_label_parking_catalog_query())
        batch: Sequence[TermsAiMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: TermsAiMark) -> TermsAiMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
