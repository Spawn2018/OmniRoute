from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.carrier_inquiry import InquiryMemberRank
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

    async def list_member_ranks(self) -> list[InquiryMemberRank]:
        answered = func.count().filter(CarrierInquiry.status == "answered")
        rows = await self._session.execute(
            select(
                CarrierInquiry.network_member_id,
                answered.label("answered_count"),
            )
            .group_by(CarrierInquiry.network_member_id)
            .order_by(answered.desc(), CarrierInquiry.network_member_id.asc()),
        )
        return [
            InquiryMemberRank(row.network_member_id, int(row.answered_count))
            for row in rows
        ]

    async def add(self, row: CarrierInquiry) -> CarrierInquiry:
        self._session.add(row)
        await self._session.flush()
        return row
