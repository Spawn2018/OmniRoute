from typing import NamedTuple
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.carrier_inquiry import InquiryMemberRank
from app.models.carrier_inquiry import CarrierInquiry
from app.models.network_member import NetworkMember
from app.models.party import Party


class InquiryDeskRow(NamedTuple):
    inquiry: CarrierInquiry
    party_id: UUID | None
    country_code: str | None


class CarrierInquiryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_recent(self) -> list[CarrierInquiry]:
        return [row.inquiry for row in await self.list_desk(overdue=False)]

    async def list_overdue(self) -> list[CarrierInquiry]:
        return [row.inquiry for row in await self.list_desk(overdue=True)]

    async def list_desk(self, *, overdue: bool) -> list[InquiryDeskRow]:
        stmt = (
            select(CarrierInquiry, NetworkMember.party_id, Party.country_code)
            .outerjoin(
                NetworkMember,
                (NetworkMember.organization_id == CarrierInquiry.organization_id)
                & (NetworkMember.id == CarrierInquiry.network_member_id),
            )
            .outerjoin(
                Party,
                (Party.organization_id == NetworkMember.organization_id)
                & (Party.id == NetworkMember.party_id),
            )
        )
        if overdue:
            stmt = stmt.where(CarrierInquiry.no_reply_after < func.current_date())
            stmt = stmt.order_by(
                CarrierInquiry.no_reply_after.asc(),
                CarrierInquiry.id,
            )
        else:
            stmt = stmt.order_by(
                CarrierInquiry.created_at.desc(),
                CarrierInquiry.id,
            )
        rows = await self._session.execute(stmt)
        return [
            InquiryDeskRow(inquiry, party_id, country_code)
            for inquiry, party_id, country_code in rows.all()
        ]

    async def get(self, inquiry_id: UUID) -> CarrierInquiry | None:
        found = await self._session.scalar(
            select(CarrierInquiry).where(CarrierInquiry.id == inquiry_id),
        )
        return found if isinstance(found, CarrierInquiry) else None

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

    async def save(self, row: CarrierInquiry) -> CarrierInquiry:
        await self._session.flush()
        return row
