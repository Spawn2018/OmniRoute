import pytest

from app.domain.errors import InvalidIngestGateMark
from app.domain.ingest_gate_mark import parse_ingest_gate_mark_row


def test_parse_ingest_gate_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_ingest_gate_mark_row(
        "ig_truth_01",
        "Truth",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("ig_truth_01", "truth", "tenant:manual")


def test_parse_ingest_gate_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidIngestGateMark, match="rodzaj"):
        parse_ingest_gate_mark_row(
            "ig_truth_01",
            "auto_accept",
            "tenant:manual",
        )
