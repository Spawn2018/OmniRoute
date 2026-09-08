from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidFieldCarryForward
from app.domain.field_carry_forward import (
    require_carry_shipment_id,
    require_field_key,
    require_field_map,
    require_field_value,
)


def test_require_field_key_accepts_allowlist() -> None:
    assert require_field_key(" incoterm ") == "incoterm"
    assert require_field_key("trade_side") == "trade_side"
    assert require_field_key("named_place") == "named_place"


def test_require_field_key_rejects_unknown() -> None:
    with pytest.raises(InvalidFieldCarryForward, match="pole"):
        require_field_key("charge_code")


def test_require_field_value_allows_empty_named_place() -> None:
    assert require_field_value("named_place", "  ") == ""
    assert require_field_value("incoterm", " FOB ") == "FOB"


def test_require_field_value_rejects_empty_incoterm() -> None:
    with pytest.raises(InvalidFieldCarryForward, match="pusta"):
        require_field_value("incoterm", "  ")


def test_require_field_map_rejects_empty_and_foreign() -> None:
    with pytest.raises(InvalidFieldCarryForward, match="brak"):
        require_field_map({})
    with pytest.raises(InvalidFieldCarryForward, match="pole"):
        require_field_map({"weight": "1"})


@given(st.sampled_from(["amount", "currency", "hs", "  "]))
def test_require_field_key_rejects_foreign_names(raw: str) -> None:
    with pytest.raises(InvalidFieldCarryForward, match="pole"):
        require_field_key(raw)


def test_require_carry_shipment_id_rejects_text() -> None:
    with pytest.raises(InvalidFieldCarryForward, match="UUID"):
        require_carry_shipment_id("ship")  # type: ignore[arg-type]


def test_require_carry_shipment_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_carry_shipment_id(token) == token
