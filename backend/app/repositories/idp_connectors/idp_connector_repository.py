from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.idp_connector import IdpConnector


class IdpConnectorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_rows(self) -> list[IdpConnector]:
        packed = await self._session.scalars(
            select(IdpConnector).order_by(
                IdpConnector.connector_code,
                IdpConnector.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: IdpConnector) -> IdpConnector:
        self._session.add(row)
        await self._session.flush()
        return row
