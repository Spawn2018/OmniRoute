from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import (
    ChannelQuoteConflict,
    InvalidChannelQuote,
    UnknownCarrierProfile,
    UnknownChannelQuote,
    UnknownPort,
)
from app.models.channel_quote import ChannelQuote
from app.services.channel_quotes.channel_quote_service import ChannelQuoteService


def _service() -> ChannelQuoteService:
    service = ChannelQuoteService(MagicMock())
    service._quotes = MagicMock()
    return service


def _row(*, party_id, origin_port_id, destination_port_id, quote_date: date) -> ChannelQuote:
    return ChannelQuote(
        id=uuid4(),
        organization_id=uuid4(),
        amount=Decimal("1200.0000"),
        currency="USD",
        party_id=party_id,
        origin_port_id=origin_port_id,
        destination_port_id=destination_port_id,
        quote_date=quote_date,
        source_ref="tenant:manual",
    )


@pytest.mark.asyncio
async def test_create_quote_requires_carrier_profile() -> None:
    service = _service()
    service._quotes.get_carrier_profile = AsyncMock(return_value=None)
    with pytest.raises(UnknownCarrierProfile, match="profilu armatora"):
        await service.create_quote(
            organization_id=uuid4(),
            user_id=uuid4(),
            party_id=uuid4(),
            origin_port_id=uuid4(),
            destination_port_id=uuid4(),
            quote_date=date(2026, 9, 1),
            amount="1200",
            currency="USD",
        )


@pytest.mark.asyncio
async def test_create_quote_unknown_port() -> None:
    service = _service()
    service._quotes.get_carrier_profile = AsyncMock(return_value=SimpleNamespace(id=uuid4()))
    service._quotes.get_port = AsyncMock(return_value=None)
    with pytest.raises(UnknownPort, match="nieznany port"):
        await service.create_quote(
            organization_id=uuid4(),
            user_id=uuid4(),
            party_id=uuid4(),
            origin_port_id=uuid4(),
            destination_port_id=uuid4(),
            quote_date=date(2026, 9, 1),
            amount="1200",
            currency="USD",
        )


@pytest.mark.asyncio
async def test_create_quote_normalizes_and_keeps_manual_origin() -> None:
    service = _service()
    party_id = uuid4()
    origin_id = uuid4()
    dest_id = uuid4()
    org_id = uuid4()

    async def add(row: ChannelQuote) -> ChannelQuote:
        return row

    service._quotes.get_carrier_profile = AsyncMock(return_value=SimpleNamespace(id=uuid4()))
    service._quotes.get_port = AsyncMock(return_value=SimpleNamespace(id=origin_id))
    service._quotes.find_as_of = AsyncMock(return_value=None)
    service._quotes.add = add
    stored = await service.create_quote(
        organization_id=org_id,
        user_id=uuid4(),
        party_id=party_id,
        origin_port_id=origin_id,
        destination_port_id=dest_id,
        quote_date=date(2026, 9, 1),
        amount="1200.5",
        currency=" usd ",
    )
    assert stored.amount == Decimal("1200.5000")
    assert stored.currency == "USD"
    assert stored.source_ref == "tenant:manual"
    assert stored.organization_id == org_id
    assert stored.party_id == party_id


@pytest.mark.asyncio
async def test_create_quote_rejects_duplicate_day() -> None:
    service = _service()
    party_id = uuid4()
    origin_id = uuid4()
    dest_id = uuid4()
    day = date(2026, 9, 1)
    service._quotes.get_carrier_profile = AsyncMock(return_value=SimpleNamespace(id=uuid4()))
    service._quotes.get_port = AsyncMock(return_value=SimpleNamespace(id=origin_id))
    service._quotes.find_as_of = AsyncMock(
        return_value=_row(
            party_id=party_id,
            origin_port_id=origin_id,
            destination_port_id=dest_id,
            quote_date=day,
        ),
    )
    with pytest.raises(ChannelQuoteConflict, match="2026-09-01"):
        await service.create_quote(
            organization_id=uuid4(),
            user_id=uuid4(),
            party_id=party_id,
            origin_port_id=origin_id,
            destination_port_id=dest_id,
            quote_date=day,
            amount="10",
            currency="USD",
        )


@pytest.mark.asyncio
async def test_create_quote_rejects_float_amount() -> None:
    service = _service()
    with pytest.raises(InvalidChannelQuote, match="float"):
        await service.create_quote(
            organization_id=uuid4(),
            user_id=uuid4(),
            party_id=uuid4(),
            origin_port_id=uuid4(),
            destination_port_id=uuid4(),
            quote_date=date(2026, 9, 1),
            amount=12.5,  # type: ignore[arg-type]
            currency="USD",
        )


@pytest.mark.asyncio
async def test_resolve_returns_row() -> None:
    service = _service()
    party_id = uuid4()
    origin_id = uuid4()
    dest_id = uuid4()
    row = _row(
        party_id=party_id,
        origin_port_id=origin_id,
        destination_port_id=dest_id,
        quote_date=date(2026, 9, 1),
    )
    service._quotes.get_carrier_profile = AsyncMock(return_value=SimpleNamespace(id=uuid4()))
    service._quotes.get_port = AsyncMock(return_value=SimpleNamespace(id=origin_id))
    service._quotes.find_as_of = AsyncMock(return_value=row)
    found = await service.resolve(
        party_id=party_id,
        origin_port_id=origin_id,
        destination_port_id=dest_id,
        on_date=date(2026, 9, 5),
    )
    assert found.id == row.id


@pytest.mark.asyncio
async def test_resolve_unknown() -> None:
    service = _service()
    service._quotes.get_carrier_profile = AsyncMock(return_value=SimpleNamespace(id=uuid4()))
    service._quotes.get_port = AsyncMock(return_value=SimpleNamespace(id=uuid4()))
    service._quotes.find_as_of = AsyncMock(return_value=None)
    with pytest.raises(UnknownChannelQuote, match="brak oferty"):
        await service.resolve(
            party_id=uuid4(),
            origin_port_id=uuid4(),
            destination_port_id=uuid4(),
            on_date=date(2026, 9, 1),
        )
