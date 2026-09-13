from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.outcome_kind import OutcomeKindDraft, parse_outcome_kind_row
from app.models.outcome_kind import OutcomeKind
from app.repositories.outcome_kinds.outcome_kind_repository import (
    OutcomeKindRepository,
)


def _as_entity(
    organization_id: UUID,
    user_id: UUID,
    draft: OutcomeKindDraft,
) -> OutcomeKind:
    return OutcomeKind(
        id=uuid4(),
        organization_id=organization_id,
        kind_code=draft.kind_code,
        source_ref=draft.source_ref,
        created_by=user_id,
    )


class OutcomeKindService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = OutcomeKindRepository(session)

    async def list_rows(self) -> list[OutcomeKind]:
        return await self._rows.list_rows()

    async def persist_kind(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        kind_code: object,
        source_ref: object,
    ) -> OutcomeKind:
        draft = parse_outcome_kind_row(kind_code, source_ref)
        return await self._rows.add(_as_entity(organization_id, user_id, draft))
