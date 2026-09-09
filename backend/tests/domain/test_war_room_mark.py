import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidWarRoomMark
from app.domain.war_room_mark import require_incident_kind, require_room_source_ref


@given(
    st.sampled_from(["weather", "congestion", "labor", "carrier", "credit", "other"])
)
def test_incident_kind_allowlist(raw: str) -> None:
    assert require_incident_kind(raw) == raw


@given(st.sampled_from(["", "chat", "WEATHER kg"]))
def test_incident_kind_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidWarRoomMark, match="incydent"):
        require_incident_kind(raw)


def test_room_source_ref_accepts_fixture() -> None:
    assert require_room_source_ref(" fixture://war-room-mark/1 ") == "fixture://war-room-mark/1"


@given(st.sampled_from(["", "   ", "http://war.example/x"]))
def test_room_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidWarRoomMark, match="obce|wskazanie"):
        require_room_source_ref(raw)
