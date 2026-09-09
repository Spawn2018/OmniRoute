from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTenderConsortiumMember
from app.domain.tender_consortium_member import (
    require_board_id,
    require_party_id,
    require_seat_code,
    require_seat_source_ref,
)


@given(st.sampled_from(["lead", "member"]))
def test_seat_code_keeps_allowlist(raw: str) -> None:
    assert require_seat_code(raw) == raw


@given(st.sampled_from(["", "X", "chair", "winner"]))
def test_seat_code_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderConsortiumMember, match="fotel"):
        require_seat_code(raw)


def test_seat_source_ref_accepts_fixture() -> None:
    assert require_seat_source_ref(" fixture://tender-consortium-member/1 ") == (
        "fixture://tender-consortium-member/1"
    )
    assert require_board_id(uuid4())
    assert require_party_id(uuid4())


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_seat_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderConsortiumMember, match="obce|wskazanie"):
        require_seat_source_ref(raw)
