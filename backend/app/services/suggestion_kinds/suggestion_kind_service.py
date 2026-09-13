from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.suggestion_kind import SuggestionKindDraft, parse_suggestion_kind_row
from app.models.suggestion_kind import SuggestionKind
from app.repositories.suggestion_kinds.suggestion_kind_repository import (
    SuggestionKindRepository,
)


def _as_entity(
    organization_id: UUID,
    user_id: UUID,
    draft: SuggestionKindDraft,
) -> SuggestionKind:
    return SuggestionKind(
        id=uuid4(),
        organization_id=organization_id,
        kind_code=draft.kind_code,
        source_ref=draft.source_ref,
        created_by=user_id,
    )


class SuggestionKindService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = SuggestionKindRepository(session)

    async def list_rows(self) -> list[SuggestionKind]:
        return await self._rows.list_rows()

    async def persist_kind(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        kind_code: object,
        source_ref: object,
    ) -> SuggestionKind:
        draft = parse_suggestion_kind_row(kind_code, source_ref)
        return await self._rows.add(_as_entity(organization_id, user_id, draft))
