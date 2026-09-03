from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fraud_flag import FraudFlag


class FraudFlagRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[FraudFlag]:
        result = await self._session.scalars(
            select(FraudFlag).order_by(FraudFlag.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: FraudFlag) -> FraudFlag:
        self._session.add(row)
        await self._session.flush()
        return row
