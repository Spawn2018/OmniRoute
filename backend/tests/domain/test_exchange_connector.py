import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidExchangeConnector
from app.domain.exchange_connector import (
    require_connector_code,
    require_exchange_source_ref,
    require_system_kind,
)


def test_connector_code_accepts_snake() -> None:
    assert require_connector_code("trans_eu_desk") == "trans_eu_desk"


def test_connector_code_rejects_bad_token() -> None:
    with pytest.raises(InvalidExchangeConnector, match="oznaczenie"):
        require_connector_code("X")
    with pytest.raises(InvalidExchangeConnector, match="oznaczenie"):
        require_connector_code(1)


@given(st.sampled_from(["trans_eu", "TRANS_EU", " Trans.eu ".replace(".", "_")]))
def test_system_kind_allowlist_trans_eu(raw: str) -> None:
    assert require_system_kind(raw) == "trans_eu"


@given(st.sampled_from(["", "timocom", "transporeon", "teleroute", "portal"]))
def test_system_kind_rejects_foreign_boards(raw: str) -> None:
    with pytest.raises(InvalidExchangeConnector, match="system"):
        require_system_kind(raw)


def test_exchange_source_ref_accepts_manual_and_fixture() -> None:
    assert require_exchange_source_ref("tenant:manual") == "tenant:manual"
    assert require_exchange_source_ref(" fixture://portal/1 ") == "fixture://portal/1"


@given(st.sampled_from(["", "   ", "https://trans.eu/x", "fixture://timocom/1"]))
def test_exchange_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidExchangeConnector, match="obce"):
        require_exchange_source_ref(raw)
