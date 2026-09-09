from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTenderRfpIntake
from app.domain.tender_rfp_intake import (
    require_board_id,
    require_intake_code,
    require_intake_source_ref,
)


@given(st.sampled_from(["scope", "deadline_gap", "incoterm_ask"]))
def test_intake_code_normalizes_snake(raw: str) -> None:
    assert require_intake_code(raw) == raw


@given(st.sampled_from(["", "X", "1band", "BAND A", "a" * 33]))
def test_intake_code_rejects_non_snake(raw: str) -> None:
    with pytest.raises(InvalidTenderRfpIntake, match="przyjęcie"):
        require_intake_code(raw)


def test_intake_source_ref_accepts_fixture() -> None:
    assert require_intake_source_ref(" fixture://tender-rfp-intake/1 ") == (
        "fixture://tender-rfp-intake/1"
    )
    assert require_board_id(uuid4())


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_intake_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderRfpIntake, match="obce|wskazanie"):
        require_intake_source_ref(raw)
