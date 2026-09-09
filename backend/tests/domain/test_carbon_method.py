import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.carbon_method import (
    require_carbon_method_source_ref,
    require_method_code,
    require_method_version,
)
from app.domain.errors import InvalidCarbonMethod


@given(st.sampled_from(["glec", "ghg_protocol", "iso_14083"]))
def test_method_code_normalizes_snake(raw: str) -> None:
    assert require_method_code(raw) == raw


@given(st.sampled_from(["", "X", "GLEC kg", "http://hold.example/x"]))
def test_method_code_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidCarbonMethod, match="metoda"):
        require_method_code(raw)


@given(st.sampled_from(["2023", "v3", "glec_2023"]))
def test_method_version_accepts_token(raw: str) -> None:
    assert require_method_version(raw) == raw


@given(st.sampled_from(["", "V 3", "http://hold.example/x"]))
def test_method_version_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidCarbonMethod, match="wersja"):
        require_method_version(raw)


def test_carbon_method_source_ref_accepts_fixture() -> None:
    assert require_carbon_method_source_ref(" fixture://carbon-method/1 ") == (
        "fixture://carbon-method/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_carbon_method_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidCarbonMethod, match="obce|wskazanie"):
        require_carbon_method_source_ref(raw)
