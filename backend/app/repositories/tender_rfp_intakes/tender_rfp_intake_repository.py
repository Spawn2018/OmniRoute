from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_rfp_intake import TenderRfpIntake


class TenderRfpIntakeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_intakes(self) -> list[TenderRfpIntake]:
        result = await self._session.scalars(
            select(TenderRfpIntake).order_by(
                TenderRfpIntake.created_at.desc(),
                TenderRfpIntake.id,
            ),
        )
        return list(result.all())

    async def add(self, row: TenderRfpIntake) -> TenderRfpIntake:
        self._session.add(row)
        await self._session.flush()
        return row
