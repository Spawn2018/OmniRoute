from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ocean_bill import OceanBill


class OceanBillRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[OceanBill]:
        result = await self._session.scalars(
            select(OceanBill).order_by(
                OceanBill.created_at.desc(),
                OceanBill.id,
            ),
        )
        return list(result.all())

    async def add(self, row: OceanBill) -> OceanBill:
        self._session.add(row)
        await self._session.flush()
        return row
