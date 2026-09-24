from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.domain.errors import IncompleteQuotationSnapshot, QuotationGap, UnknownParty, UnknownPort
from app.models.charge_code import ChargeCode
from app.models.quotation import Quotation
from app.repositories.quotations.quotation_repository import QUOTE_FROM_CURRENT_SQL
from app.services.quotations.quotation_service import (
    QuotationService,
    _snapshot_integrity_error,
)

_ROOT = Path(__file__).resolve().parents[3]
_SERVICES = _ROOT / "backend" / "app" / "services"
_REPOS = _ROOT / "backend" / "app" / "repositories"


def _catalog(*, code: str = "THC") -> ChargeCode:
    return ChargeCode(
        id=uuid4(),
        organization_id=uuid4(),
        code=code,
        name=code,
        aliases=[],
        source_ref="fixture://charge-code/test"
    )


def test_quote_sql_snapshots_lane_and_party_without_joining_catalogs() -> None:
    sql = " ".join(QUOTE_FROM_CURRENT_SQL.split())
    assert ":origin_port_id" in sql
    assert ":destination_port_id" in sql
    assert ":party_id" in sql
    assert "rl.amount" in sql
    assert "FROM rate_line" in sql
    assert "JOIN port" not in sql
    assert "JOIN party" not in sql
    assert "party_charge_override" not in sql


def test_quote_sql_does_not_filter_rate_by_port_or_party() -> None:
    sql = " ".join(QUOTE_FROM_CURRENT_SQL.split())
    assert "rl.origin_port_id" not in sql
    assert "rl.party_id" not in sql
    assert "charge_code = :charge_code" in sql.replace("rl.charge_code", "charge_code")


@pytest.mark.asyncio
async def test_quote_rejects_incomplete_snapshot_before_sql() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog())
    session.execute = AsyncMock()
    service = QuotationService(session)
    with pytest.raises(IncompleteQuotationSnapshot):
        await service.quote_from_current_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="THC",
            origin_port_id=None,
            destination_port_id=uuid4(),
            party_id=uuid4(),
        )
    session.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_quote_gap_still_wins_when_snapshot_is_complete() -> None:
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
async def test_quote_maps_party_fk_failure() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog())
    session.execute = AsyncMock(
        side_effect=IntegrityError("INSERT", {}, Exception("fk_quotation_party")),
    )
    service = QuotationService(session)
    with pytest.raises(UnknownParty, match="kontrahent"):
        await service.quote_from_current_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="THC",
            origin_port_id=uuid4(),
            destination_port_id=uuid4(),
            party_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_quote_does_not_swallow_unrelated_integrity_error() -> None:
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=_catalog())
    session.execute = AsyncMock(
        side_effect=IntegrityError("INSERT", {}, Exception("uq_something_else")),
    )
    service = QuotationService(session)
    with pytest.raises(IntegrityError):
        await service.quote_from_current_rate(
            organization_id=uuid4(),
            user_id=uuid4(),
            charge_code="THC",
            origin_port_id=uuid4(),
            destination_port_id=uuid4(),
            party_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_list_passes_filters_to_repository() -> None:
    session = AsyncMock()
    scalars = MagicMock()
    scalars.all.return_value = []
    session.scalars = AsyncMock(return_value=scalars)
    service = QuotationService(session)
    party_id = uuid4()
    origin_port_id = uuid4()
    destination_port_id = uuid4()
    listed = await service.list_quotations(
        party_id=party_id,
        origin_port_id=origin_port_id,
        destination_port_id=destination_port_id,
    )
    assert listed == []
    session.scalars.assert_awaited()


def test_quotations_do_not_import_parties_geography_or_override() -> None:
    for path in (*(_SERVICES / "quotations").rglob("*.py"), *(_REPOS / "quotations").rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        assert "app.services.parties" not in text
        assert "app.repositories.parties" not in text
        assert "app.services.geography" not in text
        assert "app.repositories.geography" not in text
        assert "party_charge_override" not in text


def _integrity(message: str) -> IntegrityError:
    return IntegrityError("INSERT", {}, Exception(message))


def test_party_fk_violation_maps_to_unknown_party() -> None:
    mapped = _snapshot_integrity_error(_integrity("fk_quotation_party"))
    assert isinstance(mapped, UnknownParty)


def test_port_fk_violation_maps_to_unknown_port() -> None:
    mapped = _snapshot_integrity_error(_integrity("fk_quotation_origin_port"))
    assert isinstance(mapped, UnknownPort)
    mapped = _snapshot_integrity_error(_integrity("fk_quotation_destination_port"))
    assert isinstance(mapped, UnknownPort)


def test_complete_check_violation_maps_to_incomplete_snapshot() -> None:
    mapped = _snapshot_integrity_error(_integrity("ck_quotation_lane_party_complete"))
    assert isinstance(mapped, IncompleteQuotationSnapshot)


def test_unrelated_integrity_error_is_not_swallowed() -> None:
    assert _snapshot_integrity_error(_integrity("uq_something_else")) is None


def test_quotation_model_has_composite_fks_and_complete_check() -> None:
    args = Quotation.__table_args__
    names = {item.name for item in args if getattr(item, "name", None)}
    assert "fk_quotation_origin_port" in names
    assert "fk_quotation_destination_port" in names
    assert "fk_quotation_party" in names
    assert "ck_quotation_lane_party_complete" in names
    columns = Quotation.__table__.c
    assert columns["origin_port_id"].nullable is True
    assert columns["destination_port_id"].nullable is True
    assert columns["party_id"].nullable is True
