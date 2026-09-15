from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.allocation_level import AllocationLevelDraft, parse_allocation_level_row
from app.models.allocation_level import AllocationLevel
from app.repositories.allocation_levels.allocation_level_repository import (
    AllocationLevelRepository,
)


def _as_entity(
    organization_id: UUID,
    user_id: UUID,
    draft: AllocationLevelDraft,
) -> AllocationLevel:
    return AllocationLevel(
        id=uuid4(),
        organization_id=organization_id,
        level_code=draft.level_code,
        source_ref=draft.source_ref,
        created_by=user_id,
    )


class AllocationLevelService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = AllocationLevelRepository(session)

    async def list_rows(self) -> list[AllocationLevel]:
        return await self._rows.list_rows()

    async def persist_level(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        level_code: object,
        source_ref: object,
    ) -> AllocationLevel:
        draft = parse_allocation_level_row(level_code, source_ref)
        return await self._rows.add(_as_entity(organization_id, user_id, draft))
