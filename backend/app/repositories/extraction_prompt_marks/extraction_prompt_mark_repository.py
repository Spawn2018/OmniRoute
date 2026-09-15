from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.extraction_prompt_mark import ExtractionPromptMark


class ExtractionPromptMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._sess = session

    async def list_marks(self) -> list[ExtractionPromptMark]:
        query = select(ExtractionPromptMark).order_by(
            ExtractionPromptMark.prompt_kind,
            ExtractionPromptMark.id,
            ExtractionPromptMark.mark_code,
        )
        return list((await self._sess.scalars(query)).all())

    async def add_mark(self, row: ExtractionPromptMark) -> ExtractionPromptMark:
        self._sess.add(row)
        await self._sess.flush()
        return row
