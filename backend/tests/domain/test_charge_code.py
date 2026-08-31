import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.charge_code import normalize_aliases, normalize_charge_code
from app.domain.errors import InvalidChargeCode

_TOKEN = st.from_regex(r"[A-Z0-9_]{2,32}", fullmatch=True)


def test_normalize_charge_code_uppercases_catalog_token() -> None:
    assert normalize_charge_code(" baf ") == "BAF"


def test_normalize_charge_code_rejects_loose_punctuation() -> None:
    with pytest.raises(InvalidChargeCode, match="2–32"):
        normalize_charge_code("THC-1")


def test_normalize_charge_code_rejects_non_text() -> None:
    with pytest.raises(InvalidChargeCode, match="tekstem"):
        normalize_charge_code(12)  # type: ignore[arg-type]


def test_normalize_aliases_dedupes_after_normalize() -> None:
    assert normalize_aliases(["bunker", "BAF", " bunker "]) == ["BUNKER", "BAF"]


@given(token=_TOKEN)
def test_normalize_charge_code_is_idempotent(token: str) -> None:
    assert normalize_charge_code(token) == token
    assert normalize_charge_code(token.lower()) == token
