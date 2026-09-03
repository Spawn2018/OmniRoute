from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.bookkeeping import (
    require_bookkeeping_charge_id,
    require_bookkeeping_invoice_id,
    require_bookkeeping_source_ref,
)
from app.domain.errors import InvalidBookkeeping


def test_require_bookkeeping_source_ref_accepts_fixture() -> None:
    assert require_bookkeeping_source_ref(" fixture://bookkeeping/1 ") == "fixture://bookkeeping/1"


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_bookkeeping_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidBookkeeping):
        require_bookkeeping_source_ref(raw)


def test_require_bookkeeping_ids_keep_uuid() -> None:
    token = uuid4()
    assert require_bookkeeping_charge_id(token) == token
    assert require_bookkeeping_invoice_id(token) == token


def test_require_bookkeeping_ids_reject_text() -> None:
    with pytest.raises(InvalidBookkeeping, match="UUID"):
        require_bookkeeping_charge_id("c")  # type: ignore[arg-type]
    with pytest.raises(InvalidBookkeeping, match="UUID"):
        require_bookkeeping_invoice_id("i")  # type: ignore[arg-type]
