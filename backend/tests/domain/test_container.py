import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.container import (
    require_container_no,
    require_container_source_ref,
    require_iso_size_type,
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


@given(st.sampled_from(["CSQU3054384", "MSCU1234567", "ABCD"]))
def test_container_no_rejects_broken_iso(raw: str) -> None:
    with pytest.raises(InvalidContainer):
        require_container_no(raw)
