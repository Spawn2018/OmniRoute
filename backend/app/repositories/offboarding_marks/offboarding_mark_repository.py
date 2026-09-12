from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.offboarding_mark import OffboardingMark


class OffboardingMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[OffboardingMark]:
        packed = await self._session.scalars(
            select(OffboardingMark).order_by(
                OffboardingMark.mark_code,
                OffboardingMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: OffboardingMark) -> OffboardingMark:
        self._session.add(row)
        await self._session.flush()
        return row
