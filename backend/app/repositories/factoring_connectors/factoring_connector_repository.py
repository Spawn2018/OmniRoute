from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.factoring_connector import FactoringConnector


class FactoringConnectorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_rows(self) -> list[FactoringConnector]:
        packed = await self._session.scalars(
            select(FactoringConnector).order_by(
                FactoringConnector.connector_code,
                FactoringConnector.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: FactoringConnector) -> FactoringConnector:
        self._session.add(row)
        await self._session.flush()
        return row
