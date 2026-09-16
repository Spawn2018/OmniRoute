from decimal import Decimal
from uuid import uuid4

import pytest

from app.domain.errors import (
    AcceptRequiresChannelQuote,
    BulkAcceptConfidenceBelow,
    ExtractionCandidatesNotEditable,
    InvalidExtractionDraft,
    InvalidTenderRfpIntake,
)
from app.domain.extraction_draft import (
    append_extraction_history,
    bulk_accept_confidence_ok,
    next_extraction_revision,
    require_bulk_accept_confidence,
    require_candidate_indexes,
    require_carrier_quote_payload,
    require_extract_path,
    require_extraction_draft_kind,
    require_rate_candidates_editable,
    require_tender_rfp_payload,
    split_candidates_by_indexes,
    undo_extraction_history,
)


def test_draft_kind_defaults_to_rate_line() -> None:
    assert require_extraction_draft_kind(None) == "rate_line"


def test_draft_kind_accepts_carrier_quote() -> None:
    assert require_extraction_draft_kind("carrier_quote") == "carrier_quote"


def test_draft_kind_accepts_tender_rfp() -> None:
    assert require_extraction_draft_kind("tender_rfp") == "tender_rfp"


def test_extract_path_defaults_to_text() -> None:
    assert require_extract_path(None) == "text"
    assert require_extract_path("image") == "image"
    with pytest.raises(InvalidExtractionDraft, match="allowlist"):
        require_extract_path("pixels")
    with pytest.raises(InvalidExtractionDraft, match="tekstem"):
        require_extract_path(1)


def test_next_extraction_revision_bumps_or_starts() -> None:
    assert next_extraction_revision(0) == 1
    assert next_extraction_revision(3) == 4
    assert next_extraction_revision(None) == 1
    assert next_extraction_revision(True) == 1


def test_append_extraction_history_starts_and_grows() -> None:
    first = append_extraction_history(
        None,
        revision=0,
        candidates=[{"code": "THC", "amount_text": "10", "currency": "EUR"}],
    )
    assert first == [
        {
            "revision": 0,
            "candidates": [{"code": "THC", "amount_text": "10", "currency": "EUR"}],
        },
    ]
    second = append_extraction_history(
        first,
        revision=1,
        candidates=[{"code": "BAF", "amount_text": "12", "currency": "USD"}],
    )
    assert len(second) == 2
    assert second[1]["revision"] == 1


def test_undo_extraction_history_restores_last_snapshot() -> None:
    history = [
        {
            "revision": 0,
            "candidates": [{"code": "THC", "amount_text": "10", "currency": "EUR"}],
        },
        {
            "revision": 1,
            "candidates": [{"code": "BAF", "amount_text": "12", "currency": "USD"}],
        },
    ]
    undone = undo_extraction_history(history)
    assert undone.revision == 1
    assert undone.candidates == [{"code": "BAF", "amount_text": "12", "currency": "USD"}]
    assert undone.history == [
        {
            "revision": 0,
            "candidates": [{"code": "THC", "amount_text": "10", "currency": "EUR"}],
        },
    ]


def test_undo_extraction_history_rejects_empty() -> None:
    with pytest.raises(InvalidExtractionDraft, match="historii"):
        undo_extraction_history([])
    with pytest.raises(InvalidExtractionDraft, match="historii"):
        undo_extraction_history(None)


def test_require_candidate_indexes_none_means_all() -> None:
    assert require_candidate_indexes(None, 3) is None


def test_require_candidate_indexes_rejects_oob_and_dup() -> None:
    with pytest.raises(InvalidExtractionDraft):
        require_candidate_indexes([0, 0], 2)
    with pytest.raises(InvalidExtractionDraft):
        require_candidate_indexes([2], 2)
    assert require_candidate_indexes([1, 0], 2) == [1, 0]


def test_split_candidates_by_indexes_partial() -> None:
    rows = ["a", "b", "c"]
    chosen, leftover = split_candidates_by_indexes(rows, [0, 2])
    assert chosen == ["a", "c"]
    assert leftover == ["b"]


def test_rate_candidates_editable_allowlist() -> None:
    require_rate_candidates_editable("rate_line")
    require_rate_candidates_editable("carrier_quote")
    require_rate_candidates_editable("tender_rfp")
    with pytest.raises(ExtractionCandidatesNotEditable, match="rate_line"):
        require_rate_candidates_editable("purchase_invoice")


def test_bulk_accept_confidence_ok_bands_and_decimal() -> None:
    assert bulk_accept_confidence_ok("0.70") is True
    assert bulk_accept_confidence_ok("0,85") is True
    assert bulk_accept_confidence_ok("85%") is True
    assert bulk_accept_confidence_ok("green") is True
    assert bulk_accept_confidence_ok("yellow") is True
    assert bulk_accept_confidence_ok("0.69") is False
    assert bulk_accept_confidence_ok("69%") is False
    assert bulk_accept_confidence_ok("orange") is False
    assert bulk_accept_confidence_ok("hold") is False
    assert bulk_accept_confidence_ok("") is False
    assert bulk_accept_confidence_ok("mystery") is False


def test_bulk_accept_gate_skips_single_candidate() -> None:
    require_bulk_accept_confidence(
        [{"code": "THC", "amount_text": "10", "currency": "EUR", "confidence_text": ""}],
    )


def test_bulk_accept_gate_blocks_low_among_many() -> None:
    with pytest.raises(BulkAcceptConfidenceBelow, match="progu zbiorczego"):
        require_bulk_accept_confidence(
            [
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
                    "confidence_text": "0.50",
                },
            ],
        )


def test_bulk_accept_gate_allows_all_high() -> None:
    require_bulk_accept_confidence(
        [
            {"code": "THC", "amount_text": "10", "currency": "EUR", "confidence_text": "high"},
            {"code": "BAF", "amount_text": "5", "currency": "EUR", "confidence_text": "0.70"},
        ],
    )


def test_bulk_accept_respects_custom_threshold() -> None:
    require_bulk_accept_confidence(
        [
            {"confidence_text": "0.90"},
            {"confidence_text": "0.80"},
        ],
        threshold=Decimal("0.80"),
    )
    with pytest.raises(BulkAcceptConfidenceBelow, match="0.80"):
        require_bulk_accept_confidence(
            [
                {"confidence_text": "0.90"},
                {"confidence_text": "0.75"},
            ],
            threshold=Decimal("0.80"),
        )


def test_draft_kind_rejects_unknown() -> None:
    with pytest.raises(InvalidExtractionDraft, match="allowlist"):
        require_extraction_draft_kind("purchase_invoice")


def test_tender_rfp_payload_reads_board_and_code() -> None:
    board = uuid4()
    stored = require_tender_rfp_payload({"tender_id": str(board), "intake_code": "scope"})
    assert stored.tender_id == board
    assert stored.intake_code == "scope"


def test_tender_rfp_payload_rejects_empty_code() -> None:
    with pytest.raises(InvalidTenderRfpIntake, match="przyjęcie"):
        require_tender_rfp_payload({"tender_id": str(uuid4()), "intake_code": "X"})


def test_carrier_quote_payload_optional_inquiry_id() -> None:
    party = uuid4()
    origin = uuid4()
    dest = uuid4()
    inquiry = uuid4()
    without = require_carrier_quote_payload(
        {
            "party_id": str(party),
            "origin_port_id": str(origin),
            "destination_port_id": str(dest),
            "quote_date": "2026-09-16",
            "amount": "10.0000",
            "currency": "USD",
        },
    )
    assert without.carrier_inquiry_id is None
    with_id = require_carrier_quote_payload(
        {
            "party_id": str(party),
            "origin_port_id": str(origin),
            "destination_port_id": str(dest),
            "quote_date": "2026-09-16",
            "amount": "10.0000",
            "currency": "USD",
            "carrier_inquiry_id": str(inquiry),
            "transit_days": 7,
        },
    )
    assert with_id.carrier_inquiry_id == inquiry
    assert with_id.transit_days == 7


def test_carrier_quote_payload_rejects_bad_inquiry_uuid() -> None:
    with pytest.raises(AcceptRequiresChannelQuote, match="UUID"):
        require_carrier_quote_payload(
            {
                "party_id": str(uuid4()),
                "origin_port_id": str(uuid4()),
                "destination_port_id": str(uuid4()),
                "quote_date": "2026-09-16",
                "amount": "10.0000",
                "currency": "USD",
                "carrier_inquiry_id": "not-a-uuid",
            },
        )
