import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidRankMark
from app.domain.rank_mark import require_rank_kind, require_rank_source_ref


@given(st.sampled_from(["price", "transit", "reliability", "carbon", "other"]))
def test_rank_kind_allowlist(raw: str) -> None:
    assert require_rank_kind(raw) == raw


@given(st.sampled_from(["", "award", "PRICE kg"]))
def test_rank_kind_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidRankMark, match="ranking"):
        require_rank_kind(raw)


def test_rank_source_ref_accepts_fixture() -> None:
    assert require_rank_source_ref(" fixture://rank-mark/1 ") == "fixture://rank-mark/1"


@given(st.sampled_from(["", "   ", "http://rank.example/x"]))
def test_rank_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidRankMark, match="obce|wskazanie"):
        require_rank_source_ref(raw)
