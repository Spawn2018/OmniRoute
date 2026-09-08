from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTenderRound
from app.domain.tender_round import require_board_id, require_round_no, require_round_source_ref


def test_round_fields_accept_positive_and_fixture() -> None:
    assert require_round_no(1) == 1
    assert require_round_source_ref(" fixture://tender-round/1 ") == "fixture://tender-round/1"
    assert require_board_id(uuid4())


def test_round_rejects_zero_and_foreign_ref() -> None:
    with pytest.raises(InvalidTenderRound, match="runda"):
        require_round_no(0)
    with pytest.raises(InvalidTenderRound, match="obce"):
        require_round_source_ref("https://evil.example/round")


@given(st.integers(max_value=0))
def test_non_positive_round_no_is_always_runda(value: int) -> None:
    with pytest.raises(InvalidTenderRound, match="runda"):
        require_round_no(value)
