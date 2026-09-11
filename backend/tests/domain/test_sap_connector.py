import pytest

from app.domain.errors import InvalidSapConnector
from app.domain.sap_connector import (
    require_connector_code,
    require_sap_source_ref,
    require_system_kind,
)


def test_require_sap_tokens_accept() -> None:
    assert require_connector_code(" sap_pl_01 ") == "sap_pl_01"
    assert require_system_kind(" SAP ") == "sap"
    assert require_system_kind("oracle") == "oracle"
    assert require_sap_source_ref("fixture://sap-connector/a") == "fixture://sap-connector/a"
    assert require_sap_source_ref("tenant:manual") == "tenant:manual"


def test_require_sap_tokens_reject() -> None:
    with pytest.raises(InvalidSapConnector, match="oznaczenie"):
        require_connector_code("X")
    with pytest.raises(InvalidSapConnector, match="system"):
        require_system_kind("optima")
    with pytest.raises(InvalidSapConnector, match="obce"):
        require_sap_source_ref("http://evil")
