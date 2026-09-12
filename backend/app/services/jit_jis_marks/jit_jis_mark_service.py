from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.jit_jis_mark import parse_jit_jis_mark_row
from app.models.jit_jis_mark import JitJisMark
from app.repositories.jit_jis_marks.jit_jis_mark_repository import (
    JitJisMarkRepository,
)


class JitJisMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = JitJisMarkRepository(session)

    async def list_marks(self) -> list[JitJisMark]:
        return await self._rows.list_marks()

    async def persist_jit_jis_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        flow_kind: object,
        source_ref: object,
    ) -> JitJisMark:
        code, kind, origin = parse_jit_jis_mark_row(
            mark_code,
            flow_kind,
            source_ref,
        )
        row = JitJisMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            flow_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
