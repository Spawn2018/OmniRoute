from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTenderWinLoss
from app.domain.tender_win_loss import (
    require_board_id,
    require_outcome,
    require_reason_code,
    require_verdict_source_ref,
)


@given(st.sampled_from(["won", "lost", "no_bid"]))
def test_outcome_keeps_allowlist(raw: str) -> None:
    assert require_outcome(raw) == raw


@given(st.sampled_from(["", "X", "awarded", "WIN"]))
def test_outcome_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderWinLoss, match="wynik"):
        require_outcome(raw)


@given(st.sampled_from(["price", "incoterm_gap", "no_capacity"]))
def test_reason_code_normalizes_snake(raw: str) -> None:
    assert require_reason_code(raw) == raw


@given(st.sampled_from(["", "X", "1band", "BAND A", "a" * 33]))
def test_reason_code_rejects_non_snake(raw: str) -> None:
    with pytest.raises(InvalidTenderWinLoss, match="powód"):
        require_reason_code(raw)


def test_verdict_source_ref_accepts_fixture() -> None:
    assert require_verdict_source_ref(" fixture://tender-win-loss/1 ") == (
        "fixture://tender-win-loss/1"
    )
    assert require_board_id(uuid4())


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_verdict_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderWinLoss, match="obce|wskazanie"):
        require_verdict_source_ref(raw)
