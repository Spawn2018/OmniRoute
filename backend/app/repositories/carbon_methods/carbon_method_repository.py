from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.carbon_method import CarbonMethod


class CarbonMethodRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_methods(self) -> list[CarbonMethod]:
        packed = await self._session.scalars(
            select(CarbonMethod).order_by(
                CarbonMethod.created_at.desc(),
                CarbonMethod.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: CarbonMethod) -> CarbonMethod:
        self._session.add(row)
        await self._session.flush()
        return row
