from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.carrier_inquiry import CarrierInquiry


class CarrierInquiryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_recent(self) -> list[CarrierInquiry]:
        rows = await self._session.scalars(
            select(CarrierInquiry).order_by(
                CarrierInquiry.created_at.desc(),
                CarrierInquiry.id,
            ),
        )
        return list(rows.all())

    async def add(self, row: CarrierInquiry) -> CarrierInquiry:
        self._session.add(row)
        await self._session.flush()
        return row
