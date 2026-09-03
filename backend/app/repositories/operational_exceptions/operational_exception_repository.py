from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.operational_exception import OperationalException


class OperationalExceptionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[OperationalException]:
        result = await self._session.scalars(
            select(OperationalException).order_by(OperationalException.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: OperationalException) -> OperationalException:
        self._session.add(row)
        await self._session.flush()
        return row
