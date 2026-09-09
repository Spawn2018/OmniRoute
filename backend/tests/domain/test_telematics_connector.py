import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTelematicsConnector
from app.domain.telematics_connector import (
    require_connector_source_ref,
    require_observation_kind,
    require_provider_code,
)


@given(st.sampled_from(["omni_telematic", "external_api"]))
def test_observation_kind_allowlist(raw: str) -> None:
    assert require_observation_kind(raw) == raw


@given(st.sampled_from(["", "fleet", "OMNI kg"]))
def test_observation_kind_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidTelematicsConnector, match="reżim"):
        require_observation_kind(raw)


@given(st.sampled_from(["gbox", "ikol", "flotis", "wialon", "other"]))
def test_provider_code_allowlist(raw: str) -> None:
    assert require_provider_code(raw) == raw


@given(st.sampled_from(["", "trans_eu", "GBOX live"]))
def test_provider_code_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidTelematicsConnector, match="dostawca"):
        require_provider_code(raw)


def test_connector_source_ref_accepts_fixture() -> None:
    assert (
        require_connector_source_ref(" fixture://telematics-connector/1 ")
        == "fixture://telematics-connector/1"
    )


@given(st.sampled_from(["", "   ", "http://gps.example/x"]))
def test_connector_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTelematicsConnector, match="obce|wskazanie"):
        require_connector_source_ref(raw)
