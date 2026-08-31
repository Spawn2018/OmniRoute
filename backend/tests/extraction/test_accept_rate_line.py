import ast
from pathlib import Path
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.api.accept_extraction import AcceptExtractionToRates
from app.domain.errors import (
    AcceptRequiresRateLine,
    InvalidMoney,
    InvalidSourceRef,
    UnknownChargeCode,
)
from app.models.extraction_draft import ExtractionDraft
from app.models.rate_line import RateLine
from app.services.extraction import extraction_service as extraction_service_mod
from app.services.extraction.extraction_service import ExtractionService

_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_FORBIDDEN_IMPORTS = (
    "app.services.rate_lines",
    "app.services.charges",
    "app.repositories.rate_lines",
    "app.repositories.charges",
    "app.models.rate_line",
    "app.models.charge",
)


def _imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            found.append(node.module)
    return found


def test_extraction_service_module_does_not_import_rates() -> None:
    assert not hasattr(extraction_service_mod, "RateLineService")
    assert not hasattr(extraction_service_mod, "RateLine")


def test_extraction_bc_does_not_import_rates_or_charges() -> None:
    roots = (
        _BACKEND_ROOT / "app" / "services" / "extraction",
        _BACKEND_ROOT / "app" / "repositories" / "extraction",
    )
    offenders: list[str] = []
    for root in roots:
        for path in root.glob("*.py"):
            for module in _imported_modules(path):
                blocked = any(
                    module == prefix or module.startswith(f"{prefix}.")
                    for prefix in _FORBIDDEN_IMPORTS
                )
                if blocked:
                    offenders.append(f"{path.as_posix()}:{module}")
    assert offenders == []


def _pending_draft(
    *,
    source_ref: str = "doc://x",
    candidates: list[dict[str, str]] | None = None,
) -> ExtractionDraft:
    rows = (
        candidates
        if candidates is not None
        else [{"code": "THC", "amount_text": "10", "currency": "EUR"}]
    )
    return ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="accepted",
        source_ref=source_ref,
        input_text="THC 10 EUR",
        payload={
            "source_ref": source_ref,
            "unparsed_regions": [],
            "candidates": rows,
        },
    )


def _rate(draft: ExtractionDraft) -> RateLine:
    return RateLine(
        id=uuid4(),
        organization_id=draft.organization_id,
        charge_code="THC",
        amount="10.0000",
        currency="EUR",
        source_ref=draft.source_ref,
    )


@pytest.mark.asyncio
async def test_accept_writes_rate_line_without_committing() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    draft = _pending_draft()
    extraction = AsyncMock()
    extraction.accept = AsyncMock(return_value=draft)
    rates = AsyncMock()
    created = _rate(draft)
    rates.create_buy_rate = AsyncMock(return_value=created)

    accepted, written = await AcceptExtractionToRates(
        session,
        extraction=extraction,
        rates=rates,
    ).accept(draft_id=draft.id, user_id=uuid4())

    assert accepted is draft
    assert written == [created]
    rates.create_buy_rate.assert_awaited_once()
    kwargs = rates.create_buy_rate.await_args.kwargs
    assert kwargs["charge_code"] == "THC"
    assert kwargs["amount"] == "10"
    assert kwargs["currency"] == "EUR"
    assert kwargs["source_ref"] == "doc://x"
    assert kwargs["organization_id"] == draft.organization_id
    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_unknown_charge_code_raises_and_does_not_commit() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    draft = _pending_draft(candidates=[{"code": "LOOSE", "amount_text": "10", "currency": "EUR"}])
    extraction = AsyncMock()
    extraction.accept = AsyncMock(return_value=draft)
    rates = AsyncMock()
    rates.create_buy_rate = AsyncMock(side_effect=UnknownChargeCode("nieznany kod opłaty: LOOSE"))

    with pytest.raises(UnknownChargeCode, match="LOOSE"):
        await AcceptExtractionToRates(session, extraction=extraction, rates=rates).accept(
            draft_id=draft.id,
            user_id=uuid4(),
        )

    session.commit.assert_not_called()
    rates.create_buy_rate.assert_awaited_once()


@pytest.mark.asyncio
async def test_second_candidate_failure_rolls_back_whole_accept() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    draft = _pending_draft(
        candidates=[
            {"code": "THC", "amount_text": "10", "currency": "EUR"},
            {"code": "XYZ", "amount_text": "1", "currency": "EUR"},
        ],
    )
    extraction = AsyncMock()
    extraction.accept = AsyncMock(return_value=draft)
    rates = AsyncMock()
    rates.create_buy_rate = AsyncMock(
        side_effect=[_rate(draft), UnknownChargeCode("nieznany kod opłaty: XYZ")],
    )

    with pytest.raises(UnknownChargeCode, match="XYZ"):
        await AcceptExtractionToRates(session, extraction=extraction, rates=rates).accept(
            draft_id=draft.id,
            user_id=uuid4(),
        )

    assert rates.create_buy_rate.await_count == 2
    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_empty_candidates_fail_closed() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    draft = _pending_draft(candidates=[])
    extraction = AsyncMock()
    extraction.accept = AsyncMock(return_value=draft)

    with pytest.raises(AcceptRequiresRateLine, match="kandydata stawki kupna"):
        await AcceptExtractionToRates(session, extraction=extraction, rates=AsyncMock()).accept(
            draft_id=draft.id,
            user_id=uuid4(),
        )

    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_blank_source_ref_fail_closed() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    draft = _pending_draft(source_ref="   ")
    extraction = AsyncMock()
    extraction.accept = AsyncMock(return_value=draft)

    with pytest.raises(InvalidSourceRef, match="obowiązkowy"):
        await AcceptExtractionToRates(session, extraction=extraction, rates=AsyncMock()).accept(
            draft_id=draft.id,
            user_id=uuid4(),
        )

    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_bad_amount_text_fail_closed() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    draft = _pending_draft(
        candidates=[{"code": "THC", "amount_text": "nie-kwota", "currency": "EUR"}],
    )
    extraction = AsyncMock()
    extraction.accept = AsyncMock(return_value=draft)
    rates = AsyncMock()
    rates.create_buy_rate = AsyncMock(side_effect=InvalidMoney("kwota nie jest liczbą dziesiętną"))

    with pytest.raises(InvalidMoney, match="dziesiętną"):
        await AcceptExtractionToRates(session, extraction=extraction, rates=rates).accept(
            draft_id=draft.id,
            user_id=uuid4(),
        )

    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_malformed_payload_fail_closed() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    draft = ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="accepted",
        source_ref="doc://x",
        input_text="x",
        payload={"candidates": "zepsute"},
    )
    extraction = AsyncMock()
    extraction.accept = AsyncMock(return_value=draft)

    with pytest.raises(AcceptRequiresRateLine, match="poprawnych kandydatów"):
        await AcceptExtractionToRates(session, extraction=extraction, rates=AsyncMock()).accept(
            draft_id=draft.id,
            user_id=uuid4(),
        )

    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_extraction_service_accept_still_only_marks_status() -> None:
    session = AsyncMock()
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    draft = ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="pending",
        source_ref="doc://x",
        input_text="THC 10 EUR",
        payload={"source_ref": "doc://x", "unparsed_regions": [], "candidates": []},
    )
    session.get = AsyncMock(return_value=draft)

    accepted = await ExtractionService(session).accept(draft_id=draft.id, user_id=uuid4())

    assert accepted.status == "accepted"
    session.commit.assert_not_called()
    session.add.assert_not_called()
