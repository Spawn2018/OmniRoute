from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cargo_claim import CargoClaim


class CargoClaimRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[CargoClaim]:
        result = await self._session.scalars(
            select(CargoClaim).order_by(CargoClaim.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: CargoClaim) -> CargoClaim:
        self._session.add(row)
        await self._session.flush()
        return row
