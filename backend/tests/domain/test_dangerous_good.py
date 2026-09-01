import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.dangerous_good import (
    normalize_imdg_class,
    normalize_un_aliases,
    normalize_un_number,
)
from app.domain.errors import InvalidDangerousGood, InvalidImdgClass

_UN = st.from_regex(r"[0-9]{4}", fullmatch=True)


def test_normalize_un_number_strips_prefix() -> None:
    assert normalize_un_number(" UN1203 ") == "1203"


def test_normalize_un_number_rejects_letters() -> None:
    with pytest.raises(InvalidDangerousGood, match="4 cyfry"):
        normalize_un_number("UN12AB")


def test_normalize_un_number_rejects_non_text() -> None:
    with pytest.raises(InvalidDangerousGood, match="tekstem"):
        normalize_un_number(1203)  # type: ignore[arg-type]


def test_normalize_imdg_class_accepts_subdivision() -> None:
    assert normalize_imdg_class(" 2.1 ") == "2.1"


def test_normalize_imdg_class_rejects_unknown() -> None:
    with pytest.raises(InvalidImdgClass, match="allowlisty"):
        normalize_imdg_class("3.9")


def test_normalize_un_aliases_dedupes() -> None:
    assert normalize_un_aliases(["1203", " UN1203 ", "1263"]) == ["1203", "1263"]


@given(token=_UN)
def test_normalize_un_number_is_idempotent(token: str) -> None:
    assert normalize_un_number(token) == token
    assert normalize_un_number(f" UN{token} ") == token
