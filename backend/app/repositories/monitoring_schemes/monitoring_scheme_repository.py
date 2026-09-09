from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.monitoring_scheme import MonitoringScheme


class MonitoringSchemeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_schemes(self) -> list[MonitoringScheme]:
        packed = await self._session.scalars(
            select(MonitoringScheme).order_by(
                MonitoringScheme.created_at.desc(),
                MonitoringScheme.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: MonitoringScheme) -> MonitoringScheme:
        self._session.add(row)
        await self._session.flush()
        return row
