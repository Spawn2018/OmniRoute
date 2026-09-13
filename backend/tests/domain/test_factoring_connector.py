import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidFactoringConnector
from app.domain.factoring_connector import (
    require_connector_code,
    require_factoring_source_ref,
    require_system_kind,
)


def test_connector_code_accepts_snake() -> None:
    assert require_connector_code("smeo_trade") == "smeo_trade"


def test_connector_code_rejects_bad_token() -> None:
    with pytest.raises(InvalidFactoringConnector, match="oznaczenie"):
        require_connector_code("X")
    with pytest.raises(InvalidFactoringConnector, match="oznaczenie"):
        require_connector_code(1)


@given(st.sampled_from(["smeo", "SMEO", " smeo ", "other", "OTHER"]))
def test_system_kind_allowlist(raw: str) -> None:
    assert require_system_kind(raw) in {"smeo", "other"}


@given(st.sampled_from(["", "stripe", "optima", "trans_eu"]))
def test_system_kind_rejects_foreign_brands(raw: str) -> None:
    with pytest.raises(InvalidFactoringConnector, match="system"):
        require_system_kind(raw)


def test_factoring_source_ref_accepts_manual_and_fixture() -> None:
    assert require_factoring_source_ref("tenant:manual") == "tenant:manual"
    assert require_factoring_source_ref(" fixture://smeo/1 ") == "fixture://smeo/1"


@given(st.sampled_from(["", "   ", "http://smeo.example/x", "fixture://optima/1"]))
def test_factoring_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidFactoringConnector, match="obce"):
        require_factoring_source_ref(raw)
