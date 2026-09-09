import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTwinMark
from app.domain.twin_mark import require_twin_kind, require_twin_source_ref


@given(
    st.sampled_from(
        ["vehicle", "driver", "container", "shipment", "network", "plan", "office", "cargo"]
    )
)
def test_twin_kind_allowlist(raw: str) -> None:
    assert require_twin_kind(raw) == raw


@given(st.sampled_from(["", "physics", "VEHICLE kg"]))
def test_twin_kind_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidTwinMark, match="postać"):
        require_twin_kind(raw)


def test_twin_source_ref_accepts_fixture() -> None:
    assert require_twin_source_ref(" fixture://twin-mark/1 ") == "fixture://twin-mark/1"


@given(st.sampled_from(["", "   ", "http://twin.example/x"]))
def test_twin_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTwinMark, match="obce|wskazanie"):
        require_twin_source_ref(raw)
