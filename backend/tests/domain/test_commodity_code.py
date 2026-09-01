import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.commodity_code import normalize_commodity_aliases, normalize_commodity_code
from app.domain.errors import InvalidCommodityCode

_TOKEN = st.from_regex(r"[0-9]{4,10}", fullmatch=True)


def test_normalize_commodity_code_strips_digits() -> None:
    assert normalize_commodity_code(" 0805 ") == "0805"


def test_normalize_commodity_code_rejects_letters() -> None:
    with pytest.raises(InvalidCommodityCode, match="4–10"):
        normalize_commodity_code("HS0805")


def test_normalize_commodity_code_rejects_non_text() -> None:
    with pytest.raises(InvalidCommodityCode, match="tekstem"):
        normalize_commodity_code(805)  # type: ignore[arg-type]


def test_normalize_commodity_aliases_dedupes() -> None:
    assert normalize_commodity_aliases(["0805", " 0805 ", "0901"]) == ["0805", "0901"]


@given(token=_TOKEN)
def test_normalize_commodity_code_is_idempotent(token: str) -> None:
    assert normalize_commodity_code(token) == token
    assert normalize_commodity_code(f" {token} ") == token
