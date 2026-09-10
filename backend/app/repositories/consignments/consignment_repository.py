from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.consignment import Consignment


class ConsignmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Consignment]:
        result = await self._session.scalars(
            select(Consignment).order_by(
                Consignment.created_at.desc(),
                Consignment.id,
            ),
        )
        return list(result.all())

    async def add(self, row: Consignment) -> Consignment:
        self._session.add(row)
        await self._session.flush()
        return row
