from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTenderAwardReview
from app.domain.tender_award_review import (
    require_board_id,
    require_review_code,
    require_review_source_ref,
)


@given(st.sampled_from(["countersign", "challenge"]))
def test_review_code_keeps_allowlist(raw: str) -> None:
    assert require_review_code(raw) == raw


@given(st.sampled_from(["", "X", "won", "AWARD"]))
def test_review_code_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderAwardReview, match="przegląd"):
        require_review_code(raw)


def test_review_source_ref_accepts_fixture() -> None:
    assert require_review_source_ref(" fixture://tender-award-review/1 ") == (
        "fixture://tender-award-review/1"
    )
    assert require_board_id(uuid4())


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_review_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderAwardReview, match="obce|wskazanie"):
        require_review_source_ref(raw)
