from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.telematics_connector import TelematicsConnector


class TelematicsConnectorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_marks(self) -> list[TelematicsConnector]:
        packed = await self._session.scalars(
            select(TelematicsConnector).order_by(
                TelematicsConnector.created_at.desc(),
                TelematicsConnector.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: TelematicsConnector) -> TelematicsConnector:
        self._session.add(row)
        await self._session.flush()
        return row
