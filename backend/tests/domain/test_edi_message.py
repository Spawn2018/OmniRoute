from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.edi_message import require_edi_kind, require_edi_shipment_id, require_edi_source_ref
from app.domain.errors import InvalidEdiMessage


def test_require_edi_kind_accepts_allowlist() -> None:
    assert require_edi_kind(" noted ") == "noted"
    assert require_edi_kind("outbound") == "outbound"
    assert require_edi_kind("other") == "other"


def test_require_edi_kind_rejects_unknown() -> None:
    with pytest.raises(InvalidEdiMessage, match="rodzaj"):
        require_edi_kind("hold")


def test_require_edi_source_ref_accepts_fixture() -> None:
    assert require_edi_source_ref(" fixture://edi-message/1 ") == "fixture://edi-message/1"


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_edi_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidEdiMessage):
        require_edi_source_ref(raw)


def test_require_edi_shipment_id_rejects_text() -> None:
    with pytest.raises(InvalidEdiMessage, match="UUID"):
        require_edi_shipment_id("msg")  # type: ignore[arg-type]


def test_require_edi_shipment_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_edi_shipment_id(token) == token
