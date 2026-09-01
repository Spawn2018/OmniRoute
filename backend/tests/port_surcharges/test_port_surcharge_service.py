from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import (
    InvalidPortSurcharge,
    PortSurchargeConflict,
    UnknownPort,
    UnknownPortSurcharge,
)
from app.models.port_surcharge import PortSurcharge
from app.services.port_surcharges.port_surcharge_service import PortSurchargeService


def _service() -> PortSurchargeService:
    service = PortSurchargeService(MagicMock())
    service._extras = MagicMock()
    return service


def _row(*, port_id, code: str = "thc") -> PortSurcharge:
    return PortSurcharge(
        id=uuid4(),
        organization_id=uuid4(),
        amount=Decimal("85.0000"),
        currency="EUR",
        port_id=port_id,
        code=code,
        title="THC",
        applies_when="kontener 40HC w weekend",
        source_ref="tenant:manual",
    )


@pytest.mark.asyncio
async def test_create_surcharge_normalizes_and_keeps_manual_origin() -> None:
    service = _service()
    port_id = uuid4()
    org_id = uuid4()

    async def add(row: PortSurcharge) -> PortSurcharge:
        return row

    service._extras.get_port = AsyncMock(return_value=SimpleNamespace(id=port_id))
    service._extras.find_by_port_and_code = AsyncMock(return_value=None)
    service._extras.add = add
    stored = await service.create_surcharge(
        organization_id=org_id,
        user_id=uuid4(),
        port_id=port_id,
        code=" THC ",
        title="  Terminal handling  ",
        applies_when="  weekend  ",
        amount="85.5",
        currency=" eur ",
    )
    assert stored.code == "thc"
    assert stored.title == "Terminal handling"
    assert stored.applies_when == "weekend"
    assert stored.amount == Decimal("85.5000")
    assert stored.currency == "EUR"
    assert stored.source_ref == "tenant:manual"
    assert stored.organization_id == org_id


@pytest.mark.asyncio
async def test_create_surcharge_unknown_port() -> None:
    service = _service()
    service._extras.get_port = AsyncMock(return_value=None)
    with pytest.raises(UnknownPort, match="nieznany port"):
        await service.create_surcharge(
            organization_id=uuid4(),
            user_id=uuid4(),
            port_id=uuid4(),
            code="thc",
            title="THC",
            applies_when="weekend",
            amount="10",
            currency="EUR",
        )


@pytest.mark.asyncio
async def test_create_surcharge_rejects_duplicate_code() -> None:
    service = _service()
    port_id = uuid4()
    service._extras.get_port = AsyncMock(return_value=SimpleNamespace(id=port_id))
    service._extras.find_by_port_and_code = AsyncMock(return_value=_row(port_id=port_id))
    with pytest.raises(PortSurchargeConflict, match="thc"):
        await service.create_surcharge(
            organization_id=uuid4(),
            user_id=uuid4(),
            port_id=port_id,
            code="thc",
            title="THC",
            applies_when="weekend",
            amount="10",
            currency="EUR",
        )


@pytest.mark.asyncio
async def test_create_surcharge_rejects_float_amount() -> None:
    service = _service()
    with pytest.raises(InvalidPortSurcharge, match="float"):
        await service.create_surcharge(
            organization_id=uuid4(),
            user_id=uuid4(),
            port_id=uuid4(),
            code="thc",
            title="THC",
            applies_when="weekend",
            amount=12.5,  # type: ignore[arg-type]
            currency="EUR",
        )


@pytest.mark.asyncio
async def test_resolve_surcharge_returns_row() -> None:
    service = _service()
    port_id = uuid4()
    row = _row(port_id=port_id)
    service._extras.get_port = AsyncMock(return_value=SimpleNamespace(id=port_id))
    service._extras.find_by_port_and_code = AsyncMock(return_value=row)
    found = await service.resolve(port_id, " THC ")
    assert found.id == row.id


@pytest.mark.asyncio
async def test_resolve_surcharge_unknown() -> None:
    service = _service()
    port_id = uuid4()
    service._extras.get_port = AsyncMock(return_value=SimpleNamespace(id=port_id))
    service._extras.find_by_port_and_code = AsyncMock(return_value=None)
    with pytest.raises(UnknownPortSurcharge, match="nieznane extra"):
        await service.resolve(port_id, "missing")
