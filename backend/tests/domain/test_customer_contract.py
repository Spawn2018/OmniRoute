import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.customer_contract import (
    fixture_opaque_blob,
    require_contract_code,
    require_contract_source_ref,
    require_shipper_label,
    require_their_customer_label,
    resolve_opaque_blob,
)
from app.domain.errors import InvalidCustomerContract


def test_contract_code_accepts_snake() -> None:
    assert require_contract_code("acme_pl_2026") == "acme_pl_2026"


def test_contract_code_rejects_bad_token() -> None:
    with pytest.raises(InvalidCustomerContract, match="oznaczenie"):
        require_contract_code("X")
    with pytest.raises(InvalidCustomerContract, match="oznaczenie"):
        require_contract_code(1)


def test_shipper_label_trims_and_accepts() -> None:
    assert require_shipper_label("  Acme Logistics  ") == "Acme Logistics"


def test_shipper_label_rejects_empty_and_long() -> None:
    with pytest.raises(InvalidCustomerContract, match="załadowca"):
        require_shipper_label("")
    with pytest.raises(InvalidCustomerContract, match="załadowca"):
        require_shipper_label("x" * 129)
    with pytest.raises(InvalidCustomerContract, match="załadowca"):
        require_shipper_label(12)


def test_their_customer_label_trims_and_accepts() -> None:
    assert require_their_customer_label("  Bayer PL  ") == "Bayer PL"


def test_their_customer_label_rejects_empty() -> None:
    with pytest.raises(InvalidCustomerContract, match="odbiorca"):
        require_their_customer_label("   ")
    with pytest.raises(InvalidCustomerContract, match="odbiorca"):
        require_their_customer_label(None)


def test_contract_source_ref_accepts_manual_and_fixture() -> None:
    assert require_contract_source_ref("tenant:manual") == "tenant:manual"
    assert require_contract_source_ref(" fixture://contract/1 ") == "fixture://contract/1"


@given(st.sampled_from(["", "   ", "https://contracts.example/x", "fixture://portal/1"]))
def test_contract_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidCustomerContract, match="obce"):
        require_contract_source_ref(raw)


def test_resolve_opaque_blob_fixture_flag_stores_constant() -> None:
    assert resolve_opaque_blob(opaque_fixture=True, opaque_blob=None) == fixture_opaque_blob()
    assert resolve_opaque_blob(opaque_fixture=False, opaque_blob=None) is None


def test_resolve_opaque_blob_accepts_fixture_base64() -> None:
    from base64 import b64encode

    packed = b64encode(b"omni-fixture-bytes").decode("ascii")
    assert resolve_opaque_blob(opaque_fixture=False, opaque_blob=packed) == b"omni-fixture-bytes"


def test_resolve_opaque_blob_rejects_bad_payload() -> None:
    with pytest.raises(InvalidCustomerContract, match="opakowanie"):
        resolve_opaque_blob(opaque_fixture="tak", opaque_blob=None)
    with pytest.raises(InvalidCustomerContract, match="opakowanie"):
        resolve_opaque_blob(opaque_fixture=False, opaque_blob="%%%")
    with pytest.raises(InvalidCustomerContract, match="opakowanie"):
        resolve_opaque_blob(opaque_fixture=False, opaque_blob=12)
