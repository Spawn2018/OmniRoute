from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTenderDataRoom
from app.domain.tender_data_room import require_board_id, require_nda_mark, require_room_source_ref


def test_room_fields_accept_signed_and_fixture() -> None:
    assert require_nda_mark(" signed ") == "signed"
    assert require_room_source_ref(" fixture://tender-data-room/1 ") == "fixture://tender-data-room/1"
    assert require_board_id(uuid4())


def test_room_rejects_pending_and_foreign_ref() -> None:
    with pytest.raises(InvalidTenderDataRoom, match="nda"):
        require_nda_mark("pending")
    with pytest.raises(InvalidTenderDataRoom, match="obce"):
        require_room_source_ref("https://evil.example/room")


@given(st.sampled_from(["", "pending", "open", "unsigned", "true"]))
def test_non_signed_nda_mark_is_always_nda(value: str) -> None:
    with pytest.raises(InvalidTenderDataRoom, match="nda"):
        require_nda_mark(value)
