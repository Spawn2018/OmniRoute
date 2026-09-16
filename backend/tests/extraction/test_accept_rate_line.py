import ast
from pathlib import Path
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.api.accept_extraction import AcceptExtractionToRates
from app.domain.errors import (
    AcceptRequiresRateLine,
    BulkAcceptConfidenceBelow,
    InvalidCarrierInquiry,
    InvalidExtractionDraft,
    InvalidMoney,
    InvalidSourceRef,
    ResourceNotFound,
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
    "app.services.channel_quotes",
    "app.models.channel_quote",
    "app.services.carrier_inquiries",
    "app.models.carrier_inquiry",
    "app.services.tender_rfp_intakes",
    "app.services.tenders",
    "app.models.tender_rfp_intake",
    "app.models.tender",
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
        status="pending",
        draft_kind="rate_line",
        source_ref=source_ref,
        input_text="THC 10 EUR",
        payload={
            "source_ref": source_ref,
            "unparsed_regions": [],
            "candidates": rows,
            "revision": 0,
            "history": [],
        },
    )


def _mock_rate_extraction(draft: ExtractionDraft) -> AsyncMock:
    extraction = AsyncMock()
    extraction.require_pending = AsyncMock(return_value=draft)
    extraction.apply_rate_accept_result = AsyncMock(return_value=draft)
    extraction.accept = AsyncMock(return_value=draft)
    return extraction


def _mock_settings(threshold: str | None = None) -> AsyncMock:
    settings = AsyncMock()
    if threshold is None:
        settings.get_setting = AsyncMock(return_value=None)
    else:
        row = AsyncMock()
        row.setting_value = threshold
        settings.get_setting = AsyncMock(return_value=row)
    return settings


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
    extraction = _mock_rate_extraction(draft)
    rates = AsyncMock()
    created = _rate(draft)
    rates.create_buy_rate = AsyncMock(return_value=created)

    outcome = await AcceptExtractionToRates(
        session,
        extraction=extraction,
        rates=rates,
        settings=_mock_settings(),
    ).accept(draft_id=draft.id, user_id=uuid4())

    assert outcome.draft is draft
    assert outcome.rate_lines == [created]
    assert outcome.channel_quotes == []
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
    extraction = _mock_rate_extraction(draft)
    rates = AsyncMock()
    rates.create_buy_rate = AsyncMock(side_effect=UnknownChargeCode("nieznany kod opĹ‚aty: LOOSE"))

    with pytest.raises(UnknownChargeCode, match="LOOSE"):
        await AcceptExtractionToRates(
            session,
            extraction=extraction,
            rates=rates,
            settings=_mock_settings(),
        ).accept(
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
            {
                "code": "THC",
                "amount_text": "10",
                "currency": "EUR",
                "confidence_text": "0.90",
            },
            {
                "code": "XYZ",
                "amount_text": "1",
                "currency": "EUR",
                "confidence_text": "0.90",
            },
        ],
    )
    extraction = _mock_rate_extraction(draft)
    rates = AsyncMock()
    rates.create_buy_rate = AsyncMock(
        side_effect=[_rate(draft), UnknownChargeCode("nieznany kod opĹ‚aty: XYZ")],
    )

    with pytest.raises(UnknownChargeCode, match="XYZ"):
        await AcceptExtractionToRates(
            session,
            extraction=extraction,
            rates=rates,
            settings=_mock_settings(),
        ).accept(
            draft_id=draft.id,
            user_id=uuid4(),
        )

    assert rates.create_buy_rate.await_count == 2
    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_bulk_accept_blocks_low_confidence_before_rates() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    draft = _pending_draft(
        candidates=[
            {
                "code": "THC",
                "amount_text": "10",
                "currency": "EUR",
                "confidence_text": "0.90",
            },
            {
                "code": "BAF",
                "amount_text": "5",
                "currency": "EUR",
                "confidence_text": "0.40",
            },
        ],
    )
    extraction = _mock_rate_extraction(draft)
    rates = AsyncMock()

    with pytest.raises(BulkAcceptConfidenceBelow, match="progu zbiorczego"):
        await AcceptExtractionToRates(
            session,
            extraction=extraction,
            rates=rates,
            settings=_mock_settings(),
        ).accept(
            draft_id=draft.id,
            user_id=uuid4(),
        )

    rates.create_buy_rate.assert_not_called()
    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_tenant_hitl_threshold_blocks_below_setting() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    draft = _pending_draft(
        candidates=[
            {
                "code": "THC",
                "amount_text": "10",
                "currency": "EUR",
                "confidence_text": "0.90",
            },
            {
                "code": "BAF",
                "amount_text": "5",
                "currency": "EUR",
                "confidence_text": "0.75",
            },
        ],
    )
    extraction = _mock_rate_extraction(draft)
    rates = AsyncMock()

    with pytest.raises(BulkAcceptConfidenceBelow, match="0.80"):
        await AcceptExtractionToRates(
            session,
            extraction=extraction,
            rates=rates,
            settings=_mock_settings("0.80"),
        ).accept(draft_id=draft.id, user_id=uuid4())

    rates.create_buy_rate.assert_not_called()


@pytest.mark.asyncio
async def test_single_low_confidence_accept_still_writes() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    draft = _pending_draft(
        candidates=[
            {
                "code": "THC",
                "amount_text": "10",
                "currency": "EUR",
                "confidence_text": "0.40",
            },
        ],
    )
    extraction = _mock_rate_extraction(draft)
    rates = AsyncMock()
    created = _rate(draft)
    rates.create_buy_rate = AsyncMock(return_value=created)

    outcome = await AcceptExtractionToRates(
        session,
        extraction=extraction,
        rates=rates,
        settings=_mock_settings(),
    ).accept(draft_id=draft.id, user_id=uuid4())

    assert outcome.rate_lines == [created]
    rates.create_buy_rate.assert_awaited_once()


@pytest.mark.asyncio
async def test_empty_candidates_fail_closed() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    draft = _pending_draft(candidates=[])
    extraction = _mock_rate_extraction(draft)

    with pytest.raises(AcceptRequiresRateLine, match="kandydat"):
        await AcceptExtractionToRates(
            session,
            extraction=extraction,
            rates=AsyncMock(),
            settings=_mock_settings(),
        ).accept(
            draft_id=draft.id,
            user_id=uuid4(),
        )

    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_blank_source_ref_fail_closed() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    draft = _pending_draft(source_ref="   ")
    extraction = _mock_rate_extraction(draft)

    with pytest.raises(InvalidSourceRef, match="source_ref"):
        await AcceptExtractionToRates(
            session,
            extraction=extraction,
            rates=AsyncMock(),
            settings=_mock_settings(),
        ).accept(
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
    extraction = _mock_rate_extraction(draft)
    rates = AsyncMock()
    rates.create_buy_rate = AsyncMock(side_effect=InvalidMoney("kwota nie jest liczba dziesietna"))

    with pytest.raises(InvalidMoney, match="kwota"):
        await AcceptExtractionToRates(
            session,
            extraction=extraction,
            rates=rates,
            settings=_mock_settings(),
        ).accept(
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
        status="pending",
        draft_kind="rate_line",
        source_ref="doc://x",
        input_text="x",
        payload={"candidates": "zepsute"},
    )
    extraction = _mock_rate_extraction(draft)

    with pytest.raises(AcceptRequiresRateLine, match="poprawnych"):
        await AcceptExtractionToRates(
            session,
            extraction=extraction,
            rates=AsyncMock(),
            settings=_mock_settings(),
        ).accept(
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


@pytest.mark.asyncio
async def test_accept_carrier_quote_writes_quote_not_rate() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    party_id = uuid4()
    origin = uuid4()
    dest = uuid4()
    draft = ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="pending",
        draft_kind="carrier_quote",
        source_ref="fixture://quote/1",
        input_text="oferta SHA-RTM",
        payload={
            "party_id": str(party_id),
            "origin_port_id": str(origin),
            "destination_port_id": str(dest),
            "quote_date": "2026-09-08",
            "amount": "10.0000",
            "currency": "USD",
            "source_ref": "fixture://quote/1",
            "unparsed_regions": [],
            "candidates": [],
        },
    )
    extraction = AsyncMock()
    extraction.require_pending = AsyncMock(return_value=draft)
    extraction.accept = AsyncMock(return_value=draft)
    rates = AsyncMock()
    quotes = AsyncMock()
    inquiries = AsyncMock()
    created = AsyncMock()
    created.id = uuid4()
    quotes.create_quote = AsyncMock(return_value=created)

    outcome = await AcceptExtractionToRates(
        session,
        extraction=extraction,
        rates=rates,
        quotes=quotes,
        inquiries=inquiries,
    ).accept(draft_id=draft.id, user_id=uuid4())

    assert outcome.rate_lines == []
    assert outcome.channel_quotes == [created]
    rates.create_buy_rate.assert_not_called()
    quotes.create_quote.assert_awaited_once()
    inquiries.mark_answered.assert_not_called()
    kwargs = quotes.create_quote.await_args.kwargs
    assert kwargs["party_id"] == party_id
    assert kwargs["source_ref"] == "fixture://quote/1"
    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_accept_carrier_quote_marks_inquiry_answered() -> None:
    session = AsyncMock()
    party_id = uuid4()
    origin = uuid4()
    dest = uuid4()
    inquiry_id = uuid4()
    draft = ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="pending",
        draft_kind="carrier_quote",
        source_ref="fixture://quote/answered",
        input_text="oferta",
        payload={
            "party_id": str(party_id),
            "origin_port_id": str(origin),
            "destination_port_id": str(dest),
            "quote_date": "2026-09-16",
            "amount": "12.5000",
            "currency": "EUR",
            "transit_days": 14,
            "carrier_inquiry_id": str(inquiry_id),
            "source_ref": "fixture://quote/answered",
            "unparsed_regions": [],
            "candidates": [],
        },
    )
    extraction = AsyncMock()
    extraction.require_pending = AsyncMock(return_value=draft)
    extraction.accept = AsyncMock(return_value=draft)
    rates = AsyncMock()
    quotes = AsyncMock()
    inquiries = AsyncMock()
    created = AsyncMock()
    created.id = uuid4()
    quotes.create_quote = AsyncMock(return_value=created)
    inquiries.mark_answered = AsyncMock(return_value=AsyncMock())

    outcome = await AcceptExtractionToRates(
        session,
        extraction=extraction,
        rates=rates,
        quotes=quotes,
        inquiries=inquiries,
    ).accept(draft_id=draft.id, user_id=uuid4())

    assert outcome.channel_quotes == [created]
    quotes.create_quote.assert_awaited_once()
    inquiries.mark_answered.assert_awaited_once_with(
        inquiry_id=inquiry_id,
        quoted_amount="12.5000",
        quoted_currency="EUR",
        quoted_transit_days=14,
    )


@pytest.mark.asyncio
async def test_accept_carrier_quote_bad_inquiry_status_rejects() -> None:
    session = AsyncMock()
    inquiry_id = uuid4()
    draft = ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="pending",
        draft_kind="carrier_quote",
        source_ref="fixture://quote/bad",
        input_text="oferta",
        payload={
            "party_id": str(uuid4()),
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "quote_date": "2026-09-16",
            "amount": "10.0000",
            "currency": "USD",
            "carrier_inquiry_id": str(inquiry_id),
            "source_ref": "fixture://quote/bad",
            "unparsed_regions": [],
            "candidates": [],
        },
    )
    extraction = AsyncMock()
    extraction.require_pending = AsyncMock(return_value=draft)
    extraction.accept = AsyncMock(return_value=draft)
    quotes = AsyncMock()
    quotes.create_quote = AsyncMock(return_value=AsyncMock(id=uuid4()))
    inquiries = AsyncMock()
    inquiries.mark_answered = AsyncMock(
        side_effect=InvalidCarrierInquiry("status zapytania nie pozwala na answered"),
    )

    with pytest.raises(InvalidCarrierInquiry, match="nie pozwala"):
        await AcceptExtractionToRates(
            session,
            extraction=extraction,
            rates=AsyncMock(),
            quotes=quotes,
            inquiries=inquiries,
        ).accept(draft_id=draft.id, user_id=uuid4())


@pytest.mark.asyncio
async def test_accept_carrier_quote_foreign_inquiry_not_found() -> None:
    session = AsyncMock()
    draft = ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="pending",
        draft_kind="carrier_quote",
        source_ref="fixture://quote/x",
        input_text="oferta",
        payload={
            "party_id": str(uuid4()),
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "quote_date": "2026-09-16",
            "amount": "10.0000",
            "currency": "USD",
            "carrier_inquiry_id": str(uuid4()),
            "source_ref": "fixture://quote/x",
            "unparsed_regions": [],
            "candidates": [],
        },
    )
    extraction = AsyncMock()
    extraction.require_pending = AsyncMock(return_value=draft)
    extraction.accept = AsyncMock(return_value=draft)
    quotes = AsyncMock()
    quotes.create_quote = AsyncMock(return_value=AsyncMock(id=uuid4()))
    inquiries = AsyncMock()
    inquiries.mark_answered = AsyncMock(side_effect=ResourceNotFound("nieznane zapytanie"))

    with pytest.raises(ResourceNotFound, match="zapytanie"):
        await AcceptExtractionToRates(
            session,
            extraction=extraction,
            rates=AsyncMock(),
            quotes=quotes,
            inquiries=inquiries,
        ).accept(draft_id=draft.id, user_id=uuid4())


@pytest.mark.asyncio
async def test_accept_tender_rfp_writes_intake_not_rate() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    board_id = uuid4()
    draft = ExtractionDraft(
        id=uuid4(),
        organization_id=uuid4(),
        status="pending",
        draft_kind="tender_rfp",
        source_ref="doc://rfp",
        input_text="RFP scope",
        payload={
            "tender_id": str(board_id),
            "intake_code": "scope",
            "source_ref": "doc://rfp",
            "unparsed_regions": [],
            "candidates": [],
        },
    )
    extraction = AsyncMock()
    extraction.require_pending = AsyncMock(return_value=draft)
    extraction.accept = AsyncMock(return_value=draft)
    rates = AsyncMock()
    quotes = AsyncMock()
    intakes = AsyncMock()
    boards = AsyncMock()
    board = AsyncMock()
    board.id = board_id
    boards.get_board = AsyncMock(return_value=board)
    created = AsyncMock()
    created.id = uuid4()
    intakes.persist_intake = AsyncMock(return_value=created)

    outcome = await AcceptExtractionToRates(
        session,
        extraction=extraction,
        rates=rates,
        quotes=quotes,
        intakes=intakes,
        boards=boards,
    ).accept(draft_id=draft.id, user_id=uuid4())

    assert outcome.rate_lines == []
    assert outcome.channel_quotes == []
    rates.create_buy_rate.assert_not_called()
    quotes.create_quote.assert_not_called()
    intakes.persist_intake.assert_awaited_once()
    kwargs = intakes.persist_intake.await_args.kwargs
    assert kwargs["tender_id"] == board_id
    assert kwargs["intake_code"] == "scope"
    assert kwargs["source_ref"] == f"fixture://tender-rfp-intake/{draft.id}"
    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_partial_accept_writes_subset_and_keeps_pending() -> None:
    session = AsyncMock()
    session.commit = AsyncMock()
    draft = _pending_draft(
        candidates=[
            {
                "code": "THC",
                "amount_text": "10",
                "currency": "EUR",
                "confidence_text": "0.90",
            },
            {
                "code": "BAF",
                "amount_text": "5",
                "currency": "EUR",
                "confidence_text": "0.40",
            },
        ],
    )
    remaining = draft.model_copy() if hasattr(draft, "model_copy") else draft
    extraction = _mock_rate_extraction(draft)
    extraction.apply_rate_accept_result = AsyncMock(return_value=remaining)
    rates = AsyncMock()
    created = _rate(draft)
    rates.create_buy_rate = AsyncMock(return_value=created)

    outcome = await AcceptExtractionToRates(
        session,
        extraction=extraction,
        rates=rates,
        settings=_mock_settings(),
    ).accept(draft_id=draft.id, user_id=uuid4(), candidate_indexes=[0])

    assert outcome.rate_lines == [created]
    rates.create_buy_rate.assert_awaited_once()
    kwargs = extraction.apply_rate_accept_result.await_args.kwargs
    assert kwargs["mark_accepted"] is False
    assert kwargs["remaining_candidates"][0]["code"] == "BAF"
    session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_partial_accept_rejects_bad_index() -> None:
    session = AsyncMock()
    draft = _pending_draft()
    extraction = _mock_rate_extraction(draft)
    rates = AsyncMock()
    with pytest.raises(InvalidExtractionDraft, match="poza zakresem"):
        await AcceptExtractionToRates(
            session,
            extraction=extraction,
            rates=rates,
            settings=_mock_settings(),
        ).accept(
            draft_id=draft.id,
            user_id=uuid4(),
            candidate_indexes=[3],
        )
    rates.create_buy_rate.assert_not_called()
