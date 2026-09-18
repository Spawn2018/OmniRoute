from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.blocks_create_enforcement_mark import (
    parse_blocks_create_enforcement_mark_row,
)
from app.models.blocks_create_enforcement_mark import BlocksCreateEnforcementMark
from app.repositories.blocks_create_enforcement_marks import (
    BlocksCreateEnforcementMarkRepository,
)


class BlocksCreateEnforcementMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = BlocksCreateEnforcementMarkRepository(session)

    async def list_marks(self) -> list[BlocksCreateEnforcementMark]:
        return await self._rows.list_marks()

    async def persist_blocks_create_enforcement_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        enforcement_kind: object,
        source_ref: object,
    ) -> BlocksCreateEnforcementMark:
        code, kind, origin = parse_blocks_create_enforcement_mark_row(
            mark_code,
            enforcement_kind,
            source_ref,
        )
        row = BlocksCreateEnforcementMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            enforcement_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
