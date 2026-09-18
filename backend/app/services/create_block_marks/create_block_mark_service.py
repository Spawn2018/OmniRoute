from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.create_block_mark import parse_create_block_mark_row
from app.models.create_block_mark import CreateBlockMark
from app.repositories.create_block_marks import CreateBlockMarkRepository


class CreateBlockMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CreateBlockMarkRepository(session)

    async def list_marks(self) -> list[CreateBlockMark]:
        return await self._rows.list_marks()

    async def persist_create_block_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        block_kind: object,
        source_ref: object,
    ) -> CreateBlockMark:
        code, kind, origin = parse_create_block_mark_row(
            mark_code,
            block_kind,
            source_ref,
        )
        row = CreateBlockMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            block_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
