import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidExecutiveMark
from app.domain.executive_mark import require_brief_source_ref, require_question_kind


@given(st.sampled_from(["loss", "lane", "risk", "cash", "other"]))
def test_question_kind_allowlist(raw: str) -> None:
    assert require_question_kind(raw) == raw


@given(st.sampled_from(["", "ebitda", "LOSS kg"]))
def test_question_kind_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidExecutiveMark, match="pytanie"):
        require_question_kind(raw)


def test_brief_source_ref_accepts_fixture() -> None:
    assert require_brief_source_ref(" fixture://executive-mark/1 ") == "fixture://executive-mark/1"


@given(st.sampled_from(["", "   ", "http://exec.example/x"]))
def test_brief_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidExecutiveMark, match="obce|wskazanie"):
        require_brief_source_ref(raw)
