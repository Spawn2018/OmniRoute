import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidNetworkCode
from app.domain.network import normalize_network_aliases, normalize_network_code

_TOKEN = st.from_regex(r"[a-z][a-z0-9_]{1,31}", fullmatch=True)


def test_normalize_network_code_lowers_and_strips() -> None:
    assert normalize_network_code(" WCA ") == "wca"


def test_normalize_network_code_replaces_hyphen() -> None:
    assert normalize_network_code("cargo-connections") == "cargo_connections"


def test_normalize_network_code_rejects_spaces_in_token() -> None:
    with pytest.raises(InvalidNetworkCode, match="snake"):
        normalize_network_code("WCA Worldwide")


def test_normalize_network_code_rejects_non_text() -> None:
    with pytest.raises(InvalidNetworkCode, match="tekstem"):
        normalize_network_code(12)  # type: ignore[arg-type]


def test_normalize_network_aliases_dedupes() -> None:
    assert normalize_network_aliases(["WCA", " wca ", "fiata"]) == ["wca", "fiata"]


@given(token=_TOKEN)
def test_normalize_network_code_is_idempotent(token: str) -> None:
    assert normalize_network_code(token) == token
    assert normalize_network_code(f" {token} ") == token
