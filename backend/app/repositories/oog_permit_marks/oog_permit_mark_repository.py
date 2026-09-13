from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.oog_permit_mark import OogPermitMark


class OogPermitMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[OogPermitMark]:
        packed = await self._session.scalars(
            select(OogPermitMark).order_by(
                OogPermitMark.mark_code,
                OogPermitMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: OogPermitMark) -> OogPermitMark:
        self._session.add(row)
        await self._session.flush()
        return row
