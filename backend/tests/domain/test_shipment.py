from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidShipment
from app.domain.shipment import (
    require_parent_pair,
    require_parent_shipment_id,
    require_party_on_quotation,
    require_quotation_id,
    require_relation_kind,
    require_shipment_ref,
    require_shipment_source_ref,
    shipment_draft_status,
)


def test_shipment_draft_status_is_draft() -> None:
    assert shipment_draft_status() == "draft"


def test_require_shipment_source_ref_accepts_fixture() -> None:
    assert (
        require_shipment_source_ref(" fixture://shipment/1 ") == "fixture://shipment/1"
    )


def test_require_shipment_source_ref_accepts_manual() -> None:
    assert require_shipment_source_ref("tenant:manual") == "tenant:manual"


@given(st.sampled_from(["", "   ", "http://lists.example/x", "ftp://x"]))
def test_require_shipment_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidShipment):
        require_shipment_source_ref(raw)


def test_require_shipment_source_ref_rejects_too_long() -> None:
    with pytest.raises(InvalidShipment, match="długie"):
        require_shipment_source_ref("fixture://shipment/" + ("a" * 250))


def test_require_quotation_id_rejects_text() -> None:
    with pytest.raises(InvalidShipment, match="UUID"):
        require_quotation_id("quote")  # type: ignore[arg-type]


def test_require_quotation_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_quotation_id(token) == token


def test_require_party_on_quotation_rejects_missing() -> None:
    with pytest.raises(InvalidShipment, match="kontrahenta"):
        require_party_on_quotation(None)


def test_require_party_on_quotation_keeps_uuid() -> None:
    token = uuid4()
    assert require_party_on_quotation(token) == token


def test_require_shipment_ref_omits_blank() -> None:
    assert require_shipment_ref(None) is None
    assert require_shipment_ref("") is None
    assert require_shipment_ref("  ") is None


@given(st.sampled_from(["fixture://shipment-ref/1", "omni://shipment/ab1"]))
def test_require_shipment_ref_allowlist(raw: str) -> None:
    assert require_shipment_ref(raw) == raw


@given(st.sampled_from(["omni://shipment/", "omni://shipment/A", "GD/2026"]))
def test_require_shipment_ref_rejects_bad_number(raw: str) -> None:
    with pytest.raises(InvalidShipment, match="numer|obce"):
        require_shipment_ref(raw)


def test_require_shipment_ref_rejects_foreign() -> None:
    with pytest.raises(InvalidShipment, match="obce"):
        require_shipment_ref("http://print.example/x")


def test_require_parent_shipment_id_omits_blank() -> None:
    assert require_parent_shipment_id(None) is None


def test_require_parent_shipment_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_parent_shipment_id(token) == token


def test_require_parent_shipment_id_rejects_text() -> None:
    with pytest.raises(InvalidShipment, match="główne"):
        require_parent_shipment_id("parent")  # type: ignore[arg-type]


def test_require_relation_kind_omits_blank() -> None:
    assert require_relation_kind(None) is None
    assert require_relation_kind("") is None
    assert require_relation_kind("  ") is None


@given(st.sampled_from(["drayage", "oncarriage", "leg_subcontract", "other"]))
def test_require_relation_kind_allowlist(raw: str) -> None:
    assert require_relation_kind(raw) == raw


@given(st.sampled_from(["margin", "sql", "consignment"]))
def test_require_relation_kind_rejects_unknown(raw: str) -> None:
    with pytest.raises(InvalidShipment, match="rodzaj"):
        require_relation_kind(raw)


def test_require_parent_pair_allows_both_empty() -> None:
    require_parent_pair(None, None, child_id=uuid4())


def test_require_parent_pair_rejects_kind_without_parent() -> None:
    with pytest.raises(InvalidShipment, match="główne"):
        require_parent_pair(None, "drayage", child_id=uuid4())


def test_require_parent_pair_rejects_parent_without_kind() -> None:
    with pytest.raises(InvalidShipment, match="rodzaj"):
        require_parent_pair(uuid4(), None, child_id=uuid4())


def test_require_parent_pair_rejects_self() -> None:
    token = uuid4()
    with pytest.raises(InvalidShipment, match="główne"):
        require_parent_pair(token, "drayage", child_id=token)
