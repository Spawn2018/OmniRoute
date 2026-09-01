from datetime import date
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import InvalidCurrency, InvalidNbpRate, NbpRateConflict, UnknownNbpRate
from app.models.nbp_rate import NbpRate
from app.services.nbp_rates.nbp_rate_service import NbpRateService


def _row(*, currency: str = "EUR", rate_date: date | None = None, mid: str = "4.2500") -> NbpRate:
    return NbpRate(
        id=uuid4(),
        organization_id=uuid4(),
        currency=currency,
        rate_date=rate_date or date(2026, 9, 1),
        mid=Decimal(mid),
        source_ref="tenant:manual",
    )


@pytest.mark.asyncio
async def test_create_normalizes_currency_and_mid() -> None:
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = NbpRateService(session)

    created = await service.create_rate(
        organization_id=uuid4(),
        user_id=uuid4(),
        currency=" eur ",
        rate_date=date(2026, 9, 1),
        mid="4.25006",
    )

    assert created.currency == "EUR"
    assert created.mid == Decimal("4.2501")
    assert created.source_ref == "tenant:manual"
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_rejects_pln() -> None:
    service = NbpRateService(AsyncMock())
    with pytest.raises(InvalidCurrency, match="PLN"):
        await service.create_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            currency="PLN",
            rate_date=date(2026, 9, 1),
            mid="1.0000",
        )


@pytest.mark.asyncio
async def test_create_rejects_float_mid() -> None:
    service = NbpRateService(AsyncMock())
    with pytest.raises(InvalidNbpRate, match="dziesiętn"):
        await service.create_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            currency="EUR",
            rate_date=date(2026, 9, 1),
            mid=4.25,  # type: ignore[arg-type]
        )


@pytest.mark.asyncio
async def test_create_rejects_duplicate_currency_date() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=_row())
    service = NbpRateService(session)
    with pytest.raises(NbpRateConflict, match="EUR"):
        await service.create_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            currency="EUR",
            rate_date=date(2026, 9, 1),
            mid="4.2600",
        )


@pytest.mark.asyncio
async def test_resolve_returns_catalog_row() -> None:
    session = AsyncMock()
    row = _row()
    session.scalar = AsyncMock(return_value=row)
    service = NbpRateService(session)

    found = await service.resolve("eur", date(2026, 9, 5))
    assert found.currency == "EUR"


@pytest.mark.asyncio
async def test_resolve_rejects_unknown_pair() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = NbpRateService(session)
    with pytest.raises(UnknownNbpRate, match="EUR"):
        await service.resolve("EUR", date(2026, 9, 1))


@pytest.mark.asyncio
async def test_list_rates_returns_repository_rows() -> None:
    session = AsyncMock()
    row = _row()
    scalars = MagicMock()
    scalars.all.return_value = [row]
    session.scalars = AsyncMock(return_value=scalars)
    service = NbpRateService(session)

    listed = await service.list_rates()
    assert listed == [row]
