from datetime import date

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.credit_review import (
    normalize_review_date,
    normalize_review_decision,
    normalize_review_note,
)
from app.domain.errors import InvalidCreditReview

_DECISIONS = st.sampled_from(["ok", "hold", "refuse"])


def test_normalize_review_decision_strips_and_lowers() -> None:
    assert normalize_review_decision(" HOLD ") == "hold"


def test_normalize_review_decision_rejects_unknown() -> None:
    with pytest.raises(InvalidCreditReview, match="ok, hold albo refuse"):
        normalize_review_decision("approve")


def test_normalize_review_decision_rejects_non_text() -> None:
    with pytest.raises(InvalidCreditReview, match="tekstem"):
        normalize_review_decision(1)


def test_normalize_review_note_empty_becomes_none() -> None:
    assert normalize_review_note("  ") is None
    assert normalize_review_note(None) is None


def test_normalize_review_note_rejects_non_text() -> None:
    with pytest.raises(InvalidCreditReview, match="tekstem"):
        normalize_review_note(12)


def test_normalize_review_note_rejects_too_long() -> None:
    with pytest.raises(InvalidCreditReview, match="za długa"):
        normalize_review_note("x" * 513)


def test_normalize_review_date_rejects_string() -> None:
    with pytest.raises(InvalidCreditReview, match="dniem"):
        normalize_review_date("2026-09-01")


def test_normalize_review_date_accepts_date() -> None:
    day = date(2026, 9, 1)
    assert normalize_review_date(day) == day


@given(token=_DECISIONS)
def test_normalize_review_decision_is_idempotent(token: str) -> None:
    assert normalize_review_decision(token) == token
    assert normalize_review_decision(f" {token.upper()} ") == token


@given(raw=st.sampled_from(["", " ", "\t", "  \n"]))
def test_empty_bureau_attachment_ref_is_rejected(raw: str) -> None:
    from app.domain.credit_review import normalize_bureau_attachment_ref

    with pytest.raises(InvalidCreditReview, match="wskazanie raportu"):
        normalize_bureau_attachment_ref(raw)


@given(n=st.integers(min_value=257, max_value=512))
def test_bureau_attachment_ref_longer_than_256_is_rejected(n: int) -> None:
    from app.domain.credit_review import normalize_bureau_attachment_ref

    with pytest.raises(InvalidCreditReview, match="za długie"):
        normalize_bureau_attachment_ref("x" * n)


@given(
    token=st.text(min_size=1, max_size=256).filter(
        lambda value: value.strip() != "" and len(value.strip()) <= 256
    ),
)
def test_bureau_attachment_ref_strips_and_stays_within_256(token: str) -> None:
    from app.domain.credit_review import normalize_bureau_attachment_ref

    stored = normalize_bureau_attachment_ref(f" {token} ")
    assert stored == token.strip()
    assert len(stored) <= 256


def test_bureau_attachment_ref_rejects_non_text() -> None:
    from app.domain.credit_review import normalize_bureau_attachment_ref

    with pytest.raises(InvalidCreditReview, match="tekstem"):
        normalize_bureau_attachment_ref(1)
