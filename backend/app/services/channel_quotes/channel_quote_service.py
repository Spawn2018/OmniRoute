from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.channel_quote import (
    manual_channel_source_ref,
    normalize_quote_amount,
    normalize_quote_currency,
    normalize_quote_date,
    normalize_transit_days,
)
from app.domain.errors import (
    ChannelQuoteConflict,
    UnknownCarrierProfile,
    UnknownChannelQuote,
    UnknownPort,
)
from app.models.channel_quote import ChannelQuote
from app.repositories.channel_quotes.channel_quote_repository import (
    ChannelQuoteCard,
    ChannelQuoteRepository,
)


def _new_channel_quote(
    *,
    organization_id: UUID,
    user_id: UUID,
    party_id: UUID,
    origin_port_id: UUID,
    destination_port_id: UUID,
    quote_date: date,
    amount: Decimal,
    currency: str,
    transit_days: int | None,
) -> ChannelQuote:
    return ChannelQuote(
        id=uuid4(),
        organization_id=organization_id,
        amount=amount,
        currency=currency,
        party_id=party_id,
        origin_port_id=origin_port_id,
        destination_port_id=destination_port_id,
        quote_date=quote_date,
        transit_days=transit_days,
        source_ref=manual_channel_source_ref(user_id),
        created_by=user_id,
    )


class ChannelQuoteService:
    def __init__(self, session: AsyncSession) -> None:
        self._quotes = ChannelQuoteRepository(session)

    async def list_quotes(self) -> list[ChannelQuote]:
        return await self._quotes.list_all()

    async def list_quote_cards(self) -> list[ChannelQuoteCard]:
        return await self._quotes.list_with_badges()

    async def get_quote(self, quote_id: UUID) -> ChannelQuote:
        found = await self._quotes.get(quote_id)
        if found is None:
            raise UnknownChannelQuote(f"nieznana oferta kanału: {quote_id}")
        return found

    async def resolve(
        self,
        *,
        party_id: UUID,
        origin_port_id: UUID,
        destination_port_id: UUID,
        on_date: object,
    ) -> ChannelQuote:
        day = normalize_quote_date(on_date)
        found = await self._lane_quote(
            party_id,
            origin_port_id,
            destination_port_id,
            day,
        )
        if found is None:
            raise UnknownChannelQuote(f"brak oferty kanału na {day.isoformat()}")
        return found

    async def _lane_quote(
        self,
        party_id: UUID,
        origin_port_id: UUID,
        destination_port_id: UUID,
        day: date,
    ) -> ChannelQuote | None:
        await self._require_carrier(party_id)
        await self._require_port(origin_port_id)
        await self._require_port(destination_port_id)
        return await self._quotes.find_as_of(
            party_id=party_id,
            origin_port_id=origin_port_id,
            destination_port_id=destination_port_id,
            on_date=day,
        )

    async def create_quote(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        origin_port_id: UUID,
        destination_port_id: UUID,
        quote_date: object,
        amount: object,
        currency: object,
        transit_days: object = None,
    ) -> ChannelQuote:
        day = normalize_quote_date(quote_date)
        stored_amount = normalize_quote_amount(amount)
        iso = normalize_quote_currency(currency)
        days = normalize_transit_days(transit_days)
        existing = await self._lane_quote(
            party_id,
            origin_port_id,
            destination_port_id,
            day,
        )
        if existing is not None and existing.quote_date == day:
            raise ChannelQuoteConflict(f"oferta na {day.isoformat()} już istnieje")
        return await self._insert_quote(
            organization_id=organization_id,
            user_id=user_id,
            party_id=party_id,
            origin_port_id=origin_port_id,
            destination_port_id=destination_port_id,
            quote_date=day,
            amount=stored_amount,
            currency=iso,
            transit_days=days,
        )

    async def _insert_quote(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        origin_port_id: UUID,
        destination_port_id: UUID,
        quote_date: date,
        amount: Decimal,
        currency: str,
        transit_days: int | None,
    ) -> ChannelQuote:
        try:
            return await self._quotes.add(
                _new_channel_quote(
                    organization_id=organization_id,
                    user_id=user_id,
                    party_id=party_id,
                    origin_port_id=origin_port_id,
                    destination_port_id=destination_port_id,
                    quote_date=quote_date,
                    amount=amount,
                    currency=currency,
                    transit_days=transit_days,
                )
            )
        except IntegrityError as exc:
            raise ChannelQuoteConflict(f"oferta na {quote_date.isoformat()} już istnieje") from exc

    async def _require_carrier(self, party_id: UUID) -> None:
        found = await self._quotes.get_carrier_profile(party_id)
        if found is None:
            raise UnknownCarrierProfile(f"brak profilu armatora: {party_id}")

    async def _require_port(self, port_id: UUID) -> None:
        found = await self._quotes.get_port(port_id)
        if found is None:
            raise UnknownPort(f"nieznany port: {port_id}")
