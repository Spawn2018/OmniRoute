from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.carrier_profile import CarrierProfile
from app.models.channel_quote import ChannelQuote
from app.models.port import Port


class ChannelQuoteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[ChannelQuote]:
        result = await self._session.scalars(
            select(ChannelQuote).order_by(ChannelQuote.quote_date.desc()),
        )
        return list(result.all())

    async def get_carrier_profile(self, party_id: UUID) -> CarrierProfile | None:
        stmt = select(CarrierProfile).where(CarrierProfile.party_id == party_id).limit(1)
        row = await self._session.scalar(stmt)
        return row if type(row) is CarrierProfile else None

    async def get_port(self, port_id: UUID) -> Port | None:
        stmt = select(Port).where(Port.id == port_id).limit(1)
        row = await self._session.scalar(stmt)
        return row if type(row) is Port else None

    async def find_as_of(
        self,
        *,
        party_id: UUID,
        origin_port_id: UUID,
        destination_port_id: UUID,
        on_date: date,
    ) -> ChannelQuote | None:
        stmt = (
            select(ChannelQuote)
            .where(
                ChannelQuote.party_id == party_id,
                ChannelQuote.origin_port_id == origin_port_id,
                ChannelQuote.destination_port_id == destination_port_id,
                ChannelQuote.quote_date <= on_date,
            )
            .order_by(ChannelQuote.quote_date.desc())
            .limit(1)
        )
        found = await self._session.scalar(stmt)
        return found if isinstance(found, ChannelQuote) else None

    async def add(self, row: ChannelQuote) -> ChannelQuote:
        self._session.add(row)
        await self._session.flush()
        return row
