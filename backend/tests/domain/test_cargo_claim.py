from datetime import date
from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.cargo_claim import (
    require_claim_kind,
    require_claim_shipment_id,
    require_claim_source_ref,
    require_cmr_notice_window,
    require_cmr_order,
    require_damage_code,
    require_notice_due_at,
    require_suit_due_at,
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


def test_require_damage_code_accepts_osd_allowlist() -> None:
    assert require_damage_code(" overage ") == "overage"
    assert require_damage_code("shortage") == "shortage"
    assert require_damage_code("damage") == "damage"
    assert require_damage_code("loss") == "loss"


def test_require_damage_code_rejects_unknown() -> None:
    with pytest.raises(InvalidCargoClaim, match="osd"):
        require_damage_code("scratch")


def test_require_cmr_notice_window_accepts_clocks() -> None:
    assert require_cmr_notice_window(" notice_7 ") == "notice_7"
    assert require_cmr_notice_window("notice_21") == "notice_21"


def test_require_cmr_notice_window_rejects_engine_token() -> None:
    with pytest.raises(InvalidCargoClaim, match="okno"):
        require_cmr_notice_window("365")


def test_require_cmr_dates_parse_iso_days() -> None:
    assert require_notice_due_at("2026-01-10") == date(2026, 1, 10)
    assert require_suit_due_at("2026-12-31") == date(2026, 12, 31)
    require_cmr_order(date(2026, 1, 10), date(2026, 12, 31))


def test_require_cmr_dates_reject_order_and_garbage() -> None:
    with pytest.raises(InvalidCargoClaim, match="zawiadomienie"):
        require_notice_due_at("10-01-2026")
    with pytest.raises(InvalidCargoClaim, match="pozew"):
        require_suit_due_at("31-12-2026")
    with pytest.raises(InvalidCargoClaim, match="kolejność"):
        require_cmr_order(date(2026, 12, 31), date(2026, 1, 10))
