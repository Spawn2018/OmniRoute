from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sap_connector import SapConnector


class SapConnectorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_connectors(self) -> list[SapConnector]:
        packed = await self._session.scalars(
            select(SapConnector).order_by(SapConnector.connector_code, SapConnector.id),
        )
        return list(packed.all())

    async def add_connector(self, row: SapConnector) -> SapConnector:
        self._session.add(row)
        await self._session.flush()
        return row
