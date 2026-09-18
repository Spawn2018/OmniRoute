from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blocks_create_enforcement_mark import BlocksCreateEnforcementMark


class BlocksCreateEnforcementMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[BlocksCreateEnforcementMark]:
        packed = await self._session.scalars(
            select(BlocksCreateEnforcementMark).order_by(
                BlocksCreateEnforcementMark.mark_code,
                BlocksCreateEnforcementMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(
        self,
        row: BlocksCreateEnforcementMark,
    ) -> BlocksCreateEnforcementMark:
        self._session.add(row)
        await self._session.flush()
        return row
