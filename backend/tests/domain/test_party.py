from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from tests.parties._load import load_attr, load_module

_ALLOWED_ROLES = (
    "customer",
    "vendor",
    "agent",
    "carrier",
    "shipper",
    "consignee",
    "notify",
)
_NIP_WEIGHTS = (6, 5, 7, 2, 3, 4, 5, 6, 7)
_NINE_DIGITS = st.from_regex(r"[0-9]{9}", fullmatch=True)
_FOREIGN_TAX = st.from_regex(r"[A-Z0-9]{2,20}", fullmatch=True)
_DOMAIN = st.from_regex(r"[A-Za-z0-9][A-Za-z0-9.-]{0,62}\.[A-Za-z]{2,16}", fullmatch=True)


def _party_domain():
    return load_module("app.domain.party")


def _invalid():
    return load_attr("app.domain.errors", "InvalidPartyData")


def _nip_checksum(nine: str) -> str:
    total = sum(int(digit) * weight for digit, weight in zip(nine, _NIP_WEIGHTS, strict=True))
    return str(total % 10)


def _valid_nip(nine: str) -> str:
    return nine + _nip_checksum(nine)


def test_unknown_party_is_a_domain_error() -> None:
    errors = load_module("app.domain.errors")
    assert hasattr(errors, "UnknownParty")
    assert issubclass(errors.UnknownParty, errors.DomainError)


def test_invalid_party_data_is_a_domain_error() -> None:
    errors = load_module("app.domain.errors")
    assert hasattr(errors, "InvalidPartyData")
    assert issubclass(errors.InvalidPartyData, errors.DomainError)


def test_polish_nip_with_valid_checksum_is_accepted() -> None:
    normalize_tax_id = _party_domain().normalize_tax_id
    assert normalize_tax_id("PL", " 123-456-32-18 ") == "1234563218"


def test_polish_nip_with_broken_checksum_is_rejected() -> None:
    with pytest.raises(_invalid(), match="NIP"):
        _party_domain().normalize_tax_id("PL", "1234563219")


def test_polish_nip_must_be_ten_digits() -> None:
    with pytest.raises(_invalid(), match="NIP"):
        _party_domain().normalize_tax_id("PL", "123456321")


@given(nine=_NINE_DIGITS)
def test_valid_polish_nip_normalize_is_idempotent(nine: str) -> None:
    normalize_tax_id = _party_domain().normalize_tax_id
    nip = _valid_nip(nine)
    assert normalize_tax_id("PL", nip) == nip
    assert normalize_tax_id("pl", f" {nip} ") == nip


@given(nine=_NINE_DIGITS)
def test_invalid_polish_nip_checksum_is_always_rejected(nine: str) -> None:
    nip = _valid_nip(nine)
    broken = nip[:9] + str((int(nip[9]) + 1) % 10)
    with pytest.raises(_invalid(), match="NIP"):
        _party_domain().normalize_tax_id("PL", broken)


@given(token=_FOREIGN_TAX)
def test_foreign_tax_id_is_casefold_and_idempotent(token: str) -> None:
    normalize_tax_id = _party_domain().normalize_tax_id
    folded = normalize_tax_id("DE", token)
    assert folded == normalize_tax_id("de", token.lower())
    assert folded == normalize_tax_id("DE", f" {token} ")
    assert folded == folded.upper()


def test_foreign_tax_id_rejects_a_blank_token() -> None:
    with pytest.raises(_invalid(), match="tax_id"):
        _party_domain().normalize_tax_id("DE", "   ")


def test_allowed_roles_are_kept_in_order_without_duplicates() -> None:
    normalize_roles = _party_domain().normalize_roles
    assert normalize_roles([" Vendor ", "customer", "vendor"]) == ["vendor", "customer"]


@given(st.lists(st.sampled_from(_ALLOWED_ROLES), min_size=1, unique=True))
def test_every_allowlisted_role_survives_normalize(roles: list[str]) -> None:
    assert _party_domain().normalize_roles(roles) == roles


def test_role_outside_the_allowlist_is_rejected() -> None:
    with pytest.raises(_invalid(), match="role"):
        _party_domain().normalize_roles(["client"])


@given(raw=_DOMAIN)
def test_email_domain_is_stored_lowercase(raw: str) -> None:
    normalize_email_domain = _party_domain().normalize_email_domain
    folded = normalize_email_domain(raw)
    assert folded == raw.strip().lower()
    assert normalize_email_domain(folded) == folded


@given(raw=_DOMAIN)
def test_address_domain_matches_stored_domain(raw: str) -> None:
    email_domain_from_address = _party_domain().email_domain_from_address
    assert email_domain_from_address(f"Ops@{raw}") == raw.strip().lower()


def test_address_without_at_is_rejected() -> None:
    with pytest.raises(_invalid(), match="@"):
        _party_domain().email_domain_from_address("acme.test")


def test_address_with_empty_local_part_is_rejected() -> None:
    with pytest.raises(_invalid(), match="lokalna"):
        _party_domain().email_domain_from_address("@acme.test")


def test_credit_pair_rejects_a_limit_without_currency() -> None:
    with pytest.raises(_invalid(), match="credit"):
        _party_domain().normalize_credit_pair(Decimal("1000.0000"), None)


def test_credit_pair_rejects_a_float_limit() -> None:
    with pytest.raises(_invalid(), match="float|kwota|credit"):
        _party_domain().normalize_credit_pair(10.5, "PLN")  # type: ignore[arg-type]


def test_manual_source_ref_is_tenant_manual() -> None:
    assert _party_domain().manual_source_ref() == "tenant:manual"


def test_accepted_lookup_source_ref_names_the_source() -> None:
    assert _party_domain().lookup_source_ref("gus") == "tenant:lookup:gus"


def test_country_code_rejects_non_text_and_wrong_length() -> None:
    with pytest.raises(_invalid(), match="country_code"):
        _party_domain().normalize_country_code(12)  # type: ignore[arg-type]
    with pytest.raises(_invalid(), match="country_code"):
        _party_domain().normalize_country_code("P")


def test_legal_name_rejects_blank() -> None:
    with pytest.raises(_invalid(), match="legal_name"):
        _party_domain().normalize_legal_name("   ")


def test_roles_reject_non_list_and_empty_after_trim() -> None:
    with pytest.raises(_invalid(), match="roles"):
        _party_domain().normalize_roles("customer")  # type: ignore[arg-type]
    with pytest.raises(_invalid(), match="roles"):
        _party_domain().normalize_roles(["  "])


def test_credit_pair_none_is_ok_and_blank_source_is_rejected() -> None:
    assert _party_domain().normalize_credit_pair(None, None) == (None, None)
    with pytest.raises(_invalid()):
        _party_domain().lookup_source_ref("  ")


@given(raw=st.sampled_from(["", " ", "\t", "http://example.test/list"]))
def test_empty_or_live_http_sanctions_ref_is_rejected(raw: str) -> None:
    with pytest.raises(_invalid(), match="wskazanie listy"):
        _party_domain().normalize_sanctions_list_ref(raw)


@given(n=st.integers(min_value=257, max_value=400))
def test_sanctions_list_ref_longer_than_256_is_rejected(n: int) -> None:
    with pytest.raises(_invalid(), match="za długie"):
        _party_domain().normalize_sanctions_list_ref("fixture://sanctions/" + ("x" * n))


@given(token=st.sampled_from(["fixture://sanctions/eu-1", "eu://consolidated"]))
def test_allowed_sanctions_list_ref_strips(token: str) -> None:
    assert _party_domain().normalize_sanctions_list_ref(f" {token} ") == token
