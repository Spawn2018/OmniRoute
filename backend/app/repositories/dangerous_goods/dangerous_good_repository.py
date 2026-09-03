from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dangerous_good import DangerousGood


class DangerousGoodRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[DangerousGood]:
        result = await self._session.scalars(
            select(DangerousGood).order_by(DangerousGood.un_number),
        )
        return list(result.all())

    async def get(self, good_id: UUID) -> DangerousGood | None:
        found = await self._session.get(DangerousGood, good_id)
        return found if isinstance(found, DangerousGood) else None

    async def find_by_token(self, token: str) -> DangerousGood | None:
        stmt = select(DangerousGood).where(
            or_(
                DangerousGood.un_number == token,
                DangerousGood.aliases.contains([token]),
            ),
        )
        found = await self._session.scalar(stmt)
        return found if isinstance(found, DangerousGood) else None

    async def add(self, row: DangerousGood) -> DangerousGood:
        self._session.add(row)
        await self._session.flush()
        return row
