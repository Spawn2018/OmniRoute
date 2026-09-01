import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.customer_sop import normalize_sop_body, normalize_sop_code, normalize_sop_title
from app.domain.errors import InvalidCustomerSop

_TOKEN = st.from_regex(r"[a-z][a-z0-9_]{1,31}", fullmatch=True)


def test_normalize_sop_code_lowers_and_strips() -> None:
    assert normalize_sop_code(" BOOKING ") == "booking"


def test_normalize_sop_code_replaces_hyphen() -> None:
    assert normalize_sop_code("pre-alert") == "pre_alert"


def test_normalize_sop_code_rejects_spaces_in_token() -> None:
    with pytest.raises(InvalidCustomerSop, match="snake"):
        normalize_sop_code("booking SOP")


def test_normalize_sop_code_rejects_non_text() -> None:
    with pytest.raises(InvalidCustomerSop, match="tekstem"):
        normalize_sop_code(12)  # type: ignore[arg-type]


def test_normalize_sop_title_collapses_space() -> None:
    assert normalize_sop_title("  Pre alert  ocean  ") == "Pre alert ocean"


def test_normalize_sop_title_rejects_blank() -> None:
    with pytest.raises(InvalidCustomerSop, match="tytuł"):
        normalize_sop_title("   ")


def test_normalize_sop_body_trims_and_rejects_blank() -> None:
    assert normalize_sop_body("  wyślij pre-alert  ") == "wyślij pre-alert"
    with pytest.raises(InvalidCustomerSop, match="treść"):
        normalize_sop_body("  ")


def test_normalize_sop_body_rejects_over_limit() -> None:
    with pytest.raises(InvalidCustomerSop, match="długa"):
        normalize_sop_body("x" * 8001)


@given(token=_TOKEN)
def test_normalize_sop_code_is_idempotent(token: str) -> None:
    assert normalize_sop_code(token) == token
    assert normalize_sop_code(f" {token} ") == token
