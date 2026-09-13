from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.autonomy_level import AutonomyLevelDraft, parse_autonomy_level_row
from app.models.autonomy_level import AutonomyLevel
from app.repositories.autonomy_levels.autonomy_level_repository import (
    AutonomyLevelRepository,
)


def _as_entity(
    organization_id: UUID,
    user_id: UUID,
    draft: AutonomyLevelDraft,
) -> AutonomyLevel:
    return AutonomyLevel(
        id=uuid4(),
        organization_id=organization_id,
        level_code=draft.level_code,
        source_ref=draft.source_ref,
        created_by=user_id,
    )


class AutonomyLevelService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = AutonomyLevelRepository(session)

    async def list_rows(self) -> list[AutonomyLevel]:
        return await self._rows.list_rows()

    async def persist_level(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        level_code: object,
        source_ref: object,
    ) -> AutonomyLevel:
        draft = parse_autonomy_level_row(level_code, source_ref)
        return await self._rows.add(_as_entity(organization_id, user_id, draft))
