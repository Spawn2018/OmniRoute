from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTenderBidStance
from app.domain.tender_bid_stance import (
    require_board_id,
    require_stance_code,
    require_stance_source_ref,
)


@given(st.sampled_from(["bid", "no_bid"]))
def test_stance_code_keeps_allowlist(raw: str) -> None:
    assert require_stance_code(raw) == raw


@given(st.sampled_from(["", "X", "won", "WIN"]))
def test_stance_code_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderBidStance, match="udział"):
        require_stance_code(raw)


def test_stance_source_ref_accepts_fixture() -> None:
    assert require_stance_source_ref(" fixture://tender-bid-stance/1 ") == (
        "fixture://tender-bid-stance/1"
    )
    assert require_board_id(uuid4())


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_stance_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderBidStance, match="obce|wskazanie"):
        require_stance_source_ref(raw)
