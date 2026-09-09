import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidMemoryEdge
from app.domain.memory_edge import require_edge_kind, require_edge_source_ref


@given(st.sampled_from(["recalls", "follows", "blocks", "cites", "other"]))
def test_edge_kind_allowlist(raw: str) -> None:
    assert require_edge_kind(raw) == raw


@given(st.sampled_from(["", "vector", "RECALLS kg"]))
def test_edge_kind_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidMemoryEdge, match="krawędź"):
        require_edge_kind(raw)


def test_edge_source_ref_accepts_fixture() -> None:
    assert require_edge_source_ref(" fixture://memory-edge/1 ") == "fixture://memory-edge/1"


@given(st.sampled_from(["", "   ", "http://memory.example/x"]))
def test_edge_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidMemoryEdge, match="obce|wskazanie"):
        require_edge_source_ref(raw)
