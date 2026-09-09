from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTenderCarbonMark
from app.domain.tender_carbon_mark import (
    require_board_id,
    require_carbon_source_ref,
    require_mark_code,
)


@given(st.sampled_from(["declared", "exempt"]))
def test_mark_code_keeps_allowlist(raw: str) -> None:
    assert require_mark_code(raw) == raw


@given(st.sampled_from(["", "X", "kg", "TCO2"]))
def test_mark_code_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderCarbonMark, match="ślad"):
        require_mark_code(raw)


def test_carbon_source_ref_accepts_fixture() -> None:
    assert require_carbon_source_ref(" fixture://tender-carbon-mark/1 ") == (
        "fixture://tender-carbon-mark/1"
    )
    assert require_board_id(uuid4())


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_carbon_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderCarbonMark, match="obce|wskazanie"):
        require_carbon_source_ref(raw)
