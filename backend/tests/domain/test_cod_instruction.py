from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.cod_instruction import (
    require_collection_status,
    require_instruction_code,
    require_instruction_shipment_id,
    require_instruction_source_ref,
)
from app.domain.errors import InvalidCodInstruction


@given(st.sampled_from(["cod_west", "cash_on_delivery", "hold_at_hub"]))
def test_instruction_code_normalizes_snake(raw: str) -> None:
    assert require_instruction_code(raw) == raw


@given(st.sampled_from(["", "X", "1cod", "COD 1", "a" * 33]))
def test_instruction_code_rejects_non_snake(raw: str) -> None:
    with pytest.raises(InvalidCodInstruction, match="snake"):
        require_instruction_code(raw)


@given(st.sampled_from(["noted", "advised", "collected", "refused"]))
def test_collection_status_allowlist(raw: str) -> None:
    assert require_collection_status(raw) == raw


@given(st.sampled_from(["paid", "pending", "settled", "invoice"]))
def test_collection_status_rejects_unknown(raw: str) -> None:
    with pytest.raises(InvalidCodInstruction, match="status"):
        require_collection_status(raw)


def test_instruction_source_ref_accepts_fixture() -> None:
    assert (
        require_instruction_source_ref(" fixture://cod-instruction/1 ")
        == "fixture://cod-instruction/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_instruction_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidCodInstruction):
        require_instruction_source_ref(raw)


def test_instruction_shipment_id_rejects_text() -> None:
    with pytest.raises(InvalidCodInstruction, match="UUID"):
        require_instruction_shipment_id("cod")  # type: ignore[arg-type]


def test_instruction_shipment_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_instruction_shipment_id(token) == token
