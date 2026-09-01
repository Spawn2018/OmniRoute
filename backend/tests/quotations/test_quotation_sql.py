from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.errors import QuotationGap, UnknownChargeCode
from app.models.charge_code import ChargeCode
from app.models.quotation import Quotation
from app.repositories.quotations.quotation_repository import QUOTE_FROM_CURRENT_SQL
from app.services.extraction import extraction_service as extraction_module
from app.services.quotations.quotation_service import QuotationService


def _catalog(*, code: str = "THC") -> ChargeCode:
    return ChargeCode(
        id=uuid4(),
        organization_id=uuid4(),
        code=code,
        name=code,
        aliases=[],
    )


def _quoted() -> Quotation:
    from decimal import Decimal

    return Quotation(
        id=uuid4(),
        organization_id=uuid4(),
        charge_code="THC",
        rate_line_id=uuid4(),
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref="tariff://a",
    )


def test_quote_sql_selects_current_rate_line_amount() -> None:
    sql = " ".join(QUOTE_FROM_CURRENT_SQL.split())
    assert "INSERT INTO quotation" in sql
    assert "SELECT" in sql
    assert "FROM rate_line" in sql
    assert "superseded_by IS NULL" in sql
    assert "rl.amount" in sql
    assert "LIMIT 1" in sql


@pytest.mark.asyncio
async def test_quote_copies_amount_from_sql_not_request() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog())
    mappings = MagicMock()
    row = _quoted()
    mappings.first.return_value = {
        "id": row.id,
        "organization_id": row.organization_id,
        "charge_code": row.charge_code,
        "rate_line_id": row.rate_line_id,
        "amount": row.amount,
        "currency": row.currency,
        "source_ref": row.source_ref,
        "created_by": None,
        "origin_port_id": None,
        "destination_port_id": None,
        "party_id": None,
    }
    execute_result = MagicMock()
    execute_result.mappings.return_value = mappings
    session.execute = AsyncMock(return_value=execute_result)
    service = QuotationService(session)

    quoted = await service.quote_from_current_rate(
        organization_id=uuid4(),
        user_id=uuid4(),
        charge_code=" thc ",
        origin_port_id=uuid4(),
        destination_port_id=uuid4(),
        party_id=uuid4(),
    )

    assert quoted.amount == row.amount
    assert quoted.currency == "EUR"
    assert quoted.charge_code == "THC"
    session.execute.assert_awaited()


@pytest.mark.asyncio
async def test_quote_gap_when_no_current_rate() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog())
    mappings = MagicMock()
    mappings.first.return_value = None
    execute_result = MagicMock()
    execute_result.mappings.return_value = mappings
    session.execute = AsyncMock(return_value=execute_result)
    service = QuotationService(session)

    with pytest.raises(QuotationGap, match="THC"):
        await service.quote_from_current_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="THC",
            origin_port_id=uuid4(),
            destination_port_id=uuid4(),
            party_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_quote_rejects_unknown_charge_code() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=None)
    service = QuotationService(session)
    with pytest.raises(UnknownChargeCode, match="LOOSE"):
        await service.quote_from_current_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="loose",
            origin_port_id=uuid4(),
            destination_port_id=uuid4(),
            party_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_list_returns_repository_rows() -> None:
    session = AsyncMock()
    row = _quoted()
    scalars = MagicMock()
    scalars.all.return_value = [row]
    session.scalars = AsyncMock(return_value=scalars)
    service = QuotationService(session)

    listed = await service.list_quotations()
    assert listed == [row]


def test_extraction_service_does_not_import_quotations() -> None:
    source = Path(extraction_module.__file__).read_text(encoding="utf-8")
    assert "from app.services.quotations" not in source
    assert "from app.repositories.quotations" not in source
    assert "from app.models.quotation" not in source
    assert "from app.services.rate_lines" not in source
    assert "from app.repositories.rate_lines" not in source
