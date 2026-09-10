import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.erp_connector import (
    require_connector_code,
    require_erp_source_ref,
    require_system_kind,
)
from app.domain.errors import InvalidErpConnector


def test_connector_code_accepts_snake() -> None:
    assert require_connector_code("optima_biuro") == "optima_biuro"


def test_connector_code_rejects_bad_token() -> None:
    with pytest.raises(InvalidErpConnector, match="oznaczenie"):
        require_connector_code("X")
    with pytest.raises(InvalidErpConnector, match="oznaczenie"):
        require_connector_code(1)


@given(st.sampled_from(["optima", "OPTIMA", " Optima "]))
def test_system_kind_allowlist_optima(raw: str) -> None:
    assert require_system_kind(raw) == "optima"


@given(st.sampled_from(["", "xl", "nexo", "gt", "symfonia", "enova"]))
def test_system_kind_rejects_foreign_brands(raw: str) -> None:
    with pytest.raises(InvalidErpConnector, match="system"):
        require_system_kind(raw)


def test_erp_source_ref_accepts_manual_and_fixture() -> None:
    assert require_erp_source_ref("tenant:manual") == "tenant:manual"
    assert require_erp_source_ref(" fixture://optima/1 ") == "fixture://optima/1"


@given(st.sampled_from(["", "   ", "http://optima.example/x", "fixture://xl/1"]))
def test_erp_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidErpConnector, match="obce"):
        require_erp_source_ref(raw)
