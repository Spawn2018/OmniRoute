from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.visibility_connector import VisibilityConnector


class VisibilityConnectorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_fixtures(self) -> list[VisibilityConnector]:
        packed = await self._session.scalars(
            select(VisibilityConnector).order_by(
                VisibilityConnector.connector_code,
                VisibilityConnector.system_kind,
                VisibilityConnector.id,
            ),
        )
        return list(packed.all())

    async def add_fixture(self, row: VisibilityConnector) -> VisibilityConnector:
        self._session.add(row)
        await self._session.flush()
        return row
