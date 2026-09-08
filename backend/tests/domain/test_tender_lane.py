from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTenderLane
from app.domain.tender_lane import require_lane_pair, require_lane_source_ref, require_lot_id


def test_lane_fields_accept_pair_and_fixture() -> None:
    origin, dest = require_lane_pair(" plgdy ", "deham")
    assert origin == "PLGDY"
    assert dest == "DEHAM"
    assert require_lane_source_ref(" fixture://tender-lane/1 ") == "fixture://tender-lane/1"
    assert require_lot_id(uuid4())


def test_lane_rejects_empty_and_foreign_ref() -> None:
    with pytest.raises(InvalidTenderLane, match="korytarz"):
        require_lane_pair("  ", "DEHAM")
    with pytest.raises(InvalidTenderLane, match="korytarz"):
        require_lane_pair("PLGDY", "PLGDY")
    with pytest.raises(InvalidTenderLane, match="obce"):
        require_lane_source_ref("https://evil.example/lane")


_UNLOCODE = st.from_regex(r"[A-Z]{2}[A-Z0-9]{3}", fullmatch=True)


@given(_UNLOCODE)
def test_identical_origin_and_destination_is_always_korytarz(code: str) -> None:
    with pytest.raises(InvalidTenderLane, match="korytarz"):
        require_lane_pair(code, code)
