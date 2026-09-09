import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.container import (
    require_cargo_description,
    require_container_no,
    require_container_ref_1,
    require_container_remarks,
    require_container_source_ref,
    require_iso_size_type,
    require_packaging_code,
    require_seal_no_1,
    require_seal_no_2,
    require_seal_no_3,
    require_vessel_name,
    require_voyage_no,
)
from app.domain.errors import InvalidContainer

_GOOD = "CSQU3054383"


def test_container_iso_and_type_allowlist() -> None:
    assert require_container_no(" csqu3054383 ") == _GOOD
    assert require_iso_size_type("45g1") == "45G1"
    assert require_container_source_ref("fixture://container/a") == "fixture://container/a"


def test_container_rejects_bad_check_digit_and_type() -> None:
    with pytest.raises(InvalidContainer, match="kontrolna"):
        require_container_no("CSQU3054384")
    with pytest.raises(InvalidContainer, match="typ ISO"):
        require_iso_size_type("HC40")
    with pytest.raises(InvalidContainer, match="obce"):
        require_container_source_ref("https://evil.example/box")


def test_seal_no_1_omits_blank_and_keeps_token() -> None:
    assert require_seal_no_1(None) is None
    assert require_seal_no_1("  ") is None
    assert require_seal_no_1(" MSC1234567 ") == "MSC1234567"


def test_seal_no_1_rejects_too_long() -> None:
    with pytest.raises(InvalidContainer, match="plomba"):
        require_seal_no_1("x" * 33)


def test_seal_no_2_reuses_same_plomba_rule() -> None:
    assert require_seal_no_2("  HL987 ") == "HL987"
    with pytest.raises(InvalidContainer, match="plomba"):
        require_seal_no_2("x" * 33)


def test_seal_no_3_reuses_same_plomba_rule() -> None:
    assert require_seal_no_3("  XY1 ") == "XY1"
    with pytest.raises(InvalidContainer, match="plomba"):
        require_seal_no_3("x" * 33)


def test_vessel_name_omits_blank_and_keeps_token() -> None:
    assert require_vessel_name(None) is None
    assert require_vessel_name("  ") is None
    assert require_vessel_name(" MSC GULSUN ") == "MSC GULSUN"
    with pytest.raises(InvalidContainer, match="statek"):
        require_vessel_name("x" * 129)


def test_voyage_no_omits_blank_and_keeps_token() -> None:
    assert require_voyage_no(None) is None
    assert require_voyage_no("  ") is None
    assert require_voyage_no(" 049W ") == "049W"
    with pytest.raises(InvalidContainer, match="rejs"):
        require_voyage_no("x" * 33)


def test_container_remarks_omits_blank_and_keeps_token() -> None:
    assert require_container_remarks(None) is None
    assert require_container_remarks("  ") is None
    assert require_container_remarks(" keep dry ") == "keep dry"
    with pytest.raises(InvalidContainer, match="uwaga"):
        require_container_remarks("x" * 257)


def test_cargo_description_omits_blank_and_keeps_token() -> None:
    assert require_cargo_description(None) is None
    assert require_cargo_description("  ") is None
    assert require_cargo_description(" steel coils ") == "steel coils"
    with pytest.raises(InvalidContainer, match="ładunek"):
        require_cargo_description("x" * 257)


def test_packaging_code_omits_blank_and_keeps_token() -> None:
    assert require_packaging_code(None) is None
    assert require_packaging_code("  ") is None
    assert require_packaging_code(" CT ") == "CT"
    with pytest.raises(InvalidContainer, match="opakowanie"):
        require_packaging_code("x" * 33)


def test_container_ref_1_omits_blank_and_keeps_token() -> None:
    assert require_container_ref_1(None) is None
    assert require_container_ref_1("  ") is None
    assert require_container_ref_1(" PO123 ") == "PO123"
    with pytest.raises(InvalidContainer, match="referencja"):
        require_container_ref_1("x" * 65)


@given(st.sampled_from(["CSQU3054384", "MSCU1234567", "ABCD"]))
def test_container_no_rejects_broken_iso(raw: str) -> None:
    with pytest.raises(InvalidContainer):
        require_container_no(raw)
