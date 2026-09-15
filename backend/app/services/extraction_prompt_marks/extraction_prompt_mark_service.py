from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.extraction_prompt_mark import parse_extraction_prompt_mark_row
from app.models.extraction_prompt_mark import ExtractionPromptMark
from app.repositories.extraction_prompt_marks.extraction_prompt_mark_repository import (
    ExtractionPromptMarkRepository,
)


class ExtractionPromptMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = ExtractionPromptMarkRepository(session)

    async def list_marks(self) -> list[ExtractionPromptMark]:
        return await self._repo.list_marks()

    async def persist_extraction_prompt_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        prompt_kind: object,
        source_ref: object,
    ) -> ExtractionPromptMark:
        code, kind, origin = parse_extraction_prompt_mark_row(
            mark_code,
            prompt_kind,
            source_ref,
        )
        return await self._repo.add_mark(
            ExtractionPromptMark(
                id=uuid4(),
                organization_id=organization_id,
                mark_code=code,
                prompt_kind=kind,
                source_ref=origin,
                created_by=user_id,
            ),
        )
