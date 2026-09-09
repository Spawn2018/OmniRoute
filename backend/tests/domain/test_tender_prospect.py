from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTenderProspect
from app.domain.tender_prospect import (
    require_board_id,
    require_outreach_code,
    require_party_id,
    require_prospect_source_ref,
)


@given(st.sampled_from(["called", "emailed", "meeting"]))
def test_outreach_code_normalizes_snake(raw: str) -> None:
    assert require_outreach_code(raw) == raw


@given(st.sampled_from(["", "X", "1band", "BAND A", "a" * 33]))
def test_outreach_code_rejects_non_snake(raw: str) -> None:
    with pytest.raises(InvalidTenderProspect, match="prospekt"):
        require_outreach_code(raw)


def test_prospect_source_ref_accepts_fixture() -> None:
    assert require_prospect_source_ref(" fixture://tender-prospect/1 ") == (
        "fixture://tender-prospect/1"
    )
    assert require_board_id(uuid4())
    assert require_party_id(uuid4())


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_prospect_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderProspect, match="obce|wskazanie"):
        require_prospect_source_ref(raw)
