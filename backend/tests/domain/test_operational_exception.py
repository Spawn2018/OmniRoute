from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidOperationalException
from app.domain.operational_exception import (
    require_exception_kind,
    require_exception_shipment_id,
    require_exception_source_ref,
)


def test_require_exception_kind_accepts_allowlist() -> None:
    assert require_exception_kind(" noted ") == "noted"
    assert require_exception_kind("blocked") == "blocked"
    assert require_exception_kind("other") == "other"


def test_require_exception_kind_rejects_unknown() -> None:
    with pytest.raises(InvalidOperationalException, match="rodzaj"):
        require_exception_kind("hold")


def test_require_exception_source_ref_accepts_fixture() -> None:
    assert (
        require_exception_source_ref(" fixture://operational-exception/1 ")
        == "fixture://operational-exception/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_exception_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidOperationalException):
        require_exception_source_ref(raw)


def test_require_exception_shipment_id_rejects_text() -> None:
    with pytest.raises(InvalidOperationalException, match="UUID"):
        require_exception_shipment_id("exc")  # type: ignore[arg-type]


def test_require_exception_shipment_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_exception_shipment_id(token) == token
