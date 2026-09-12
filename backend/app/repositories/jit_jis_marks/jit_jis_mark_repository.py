from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.jit_jis_mark import JitJisMark


class JitJisMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[JitJisMark]:
        packed = await self._session.scalars(
            select(JitJisMark).order_by(
                JitJisMark.mark_code,
                JitJisMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: JitJisMark) -> JitJisMark:
        self._session.add(row)
        await self._session.flush()
        return row
