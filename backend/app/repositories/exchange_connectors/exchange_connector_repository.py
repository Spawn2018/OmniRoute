from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exchange_connector import ExchangeConnector


class ExchangeConnectorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_rows(self) -> list[ExchangeConnector]:
        packed = await self._session.scalars(
            select(ExchangeConnector).order_by(
                ExchangeConnector.connector_code,
                ExchangeConnector.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: ExchangeConnector) -> ExchangeConnector:
        self._session.add(row)
        await self._session.flush()
        return row
