from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.erp_connector import ErpConnector


class ErpConnectorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_rows(self) -> list[ErpConnector]:
        packed = await self._session.scalars(
            select(ErpConnector).order_by(
                ErpConnector.connector_code,
                ErpConnector.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: ErpConnector) -> ErpConnector:
        self._session.add(row)
        await self._session.flush()
        return row
