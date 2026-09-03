from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.cost_to_serve import (
    require_cost_to_serve_quotation_id,
    require_cost_to_serve_sop_id,
    require_cost_to_serve_source_ref,
)
from app.domain.errors import InvalidCostToServe


def test_require_cost_to_serve_source_ref_accepts_fixture() -> None:
    assert (
        require_cost_to_serve_source_ref(" fixture://cost-to-serve/1 ")
        == "fixture://cost-to-serve/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_cost_to_serve_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidCostToServe):
        require_cost_to_serve_source_ref(raw)


def test_require_cost_to_serve_ids_keep_uuid() -> None:
    token = uuid4()
    assert require_cost_to_serve_sop_id(token) == token
    assert require_cost_to_serve_quotation_id(token) == token


def test_require_cost_to_serve_ids_reject_text() -> None:
    with pytest.raises(InvalidCostToServe, match="UUID"):
        require_cost_to_serve_sop_id("s")  # type: ignore[arg-type]
    with pytest.raises(InvalidCostToServe, match="UUID"):
        require_cost_to_serve_quotation_id("q")  # type: ignore[arg-type]
