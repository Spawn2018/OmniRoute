from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.twin_kind import TwinKindDraft, parse_twin_kind_row
from app.models.twin_kind import TwinKind
from app.repositories.twin_kinds.twin_kind_repository import TwinKindRepository


def _as_entity(organization_id: UUID, user_id: UUID, draft: TwinKindDraft) -> TwinKind:
    return TwinKind(
        id=uuid4(),
        organization_id=organization_id,
        kind_code=draft.kind_code,
        source_ref=draft.source_ref,
        created_by=user_id,
    )


class TwinKindService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TwinKindRepository(session)

    async def list_rows(self) -> list[TwinKind]:
        return await self._rows.list_rows()

    async def persist_kind(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        kind_code: object,
        source_ref: object,
    ) -> TwinKind:
        draft = parse_twin_kind_row(kind_code, source_ref)
        return await self._rows.add(_as_entity(organization_id, user_id, draft))
