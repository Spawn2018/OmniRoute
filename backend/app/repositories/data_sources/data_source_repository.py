from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.data_source import DataSource


class DataSourceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[DataSource]:
        stmt = select(DataSource).order_by(
            DataSource.source_code,
            DataSource.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: DataSource) -> DataSource:
        self._session.add(row)
        await self._session.flush()
        return row
