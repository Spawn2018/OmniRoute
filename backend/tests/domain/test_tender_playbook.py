from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTenderPlaybook
from app.domain.tender_playbook import (
    require_board_id,
    require_claim_code,
    require_claim_text,
    require_play_source_ref,
)


@given(st.sampled_from(["incoterm_fob", "no_dg", "weekend_gate"]))
def test_claim_code_normalizes_snake(raw: str) -> None:
    assert require_claim_code(raw) == raw


@given(st.sampled_from(["", "X", "1band", "BAND A", "a" * 33]))
def test_claim_code_rejects_non_snake(raw: str) -> None:
    with pytest.raises(InvalidTenderPlaybook, match="teza"):
        require_claim_code(raw)


@given(st.sampled_from(["tylko FOB", "brak DG na tej partii"]))
def test_claim_text_keeps_body(raw: str) -> None:
    assert require_claim_text(raw) == raw


@given(st.sampled_from(["", "   ", "x" * 513]))
def test_claim_text_rejects_empty_and_long(raw: str) -> None:
    with pytest.raises(InvalidTenderPlaybook, match="twierdzenie"):
        require_claim_text(raw)


def test_play_source_ref_accepts_fixture() -> None:
    assert require_play_source_ref(" fixture://tender-playbook/1 ") == "fixture://tender-playbook/1"
    assert require_board_id(uuid4())


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_play_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderPlaybook, match="obce|wskazanie"):
        require_play_source_ref(raw)
