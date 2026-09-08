from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.local_charge import LocalCharge


class LocalChargeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[LocalCharge]:
        result = await self._session.scalars(
            select(LocalCharge).order_by(LocalCharge.created_at.desc(), LocalCharge.id),
        )
        return list(result.all())

    async def add(self, row: LocalCharge) -> LocalCharge:
        self._session.add(row)
        await self._session.flush()
        return row
