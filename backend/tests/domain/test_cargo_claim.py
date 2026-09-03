from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.cargo_claim import (
    require_claim_kind,
    require_claim_shipment_id,
    require_claim_source_ref,
)
from app.domain.errors import InvalidCargoClaim


def test_require_claim_kind_accepts_allowlist() -> None:
    assert require_claim_kind(" damage ") == "damage"
    assert require_claim_kind("shortage") == "shortage"
    assert require_claim_kind("other") == "other"


def test_require_claim_kind_rejects_unknown() -> None:
    with pytest.raises(InvalidCargoClaim, match="rodzaj"):
        require_claim_kind("fraud")


def test_require_claim_source_ref_accepts_fixture() -> None:
    assert require_claim_source_ref(" fixture://cargo-claim/1 ") == "fixture://cargo-claim/1"


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_claim_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidCargoClaim):
        require_claim_source_ref(raw)


def test_require_claim_shipment_id_rejects_text() -> None:
    with pytest.raises(InvalidCargoClaim, match="UUID"):
        require_claim_shipment_id("claim")  # type: ignore[arg-type]


def test_require_claim_shipment_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_claim_shipment_id(token) == token
