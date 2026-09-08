from decimal import Decimal
from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTenderMatrixCell
from app.domain.tender_matrix_cell import (
    require_board_id,
    require_cell_amount,
    require_cell_code,
    require_cell_currency,
    require_cell_source_ref,
)


@given(st.sampled_from(["ocean_fcl", "thc_origin", "band_west"]))
def test_cell_code_normalizes_snake(raw: str) -> None:
    assert require_cell_code(raw) == raw


@given(st.sampled_from(["", "X", "1band", "BAND A", "a" * 33]))
def test_cell_code_rejects_non_snake(raw: str) -> None:
    with pytest.raises(InvalidTenderMatrixCell, match="komórka"):
        require_cell_code(raw)


def test_cell_amount_rejects_float() -> None:
    with pytest.raises(InvalidTenderMatrixCell, match="kwota"):
        require_cell_amount(12.5)  # type: ignore[arg-type]


def test_cell_amount_rejects_bool() -> None:
    with pytest.raises(InvalidTenderMatrixCell, match="kwota"):
        require_cell_amount(True)  # type: ignore[arg-type]


def test_cell_amount_rejects_zero() -> None:
    with pytest.raises(InvalidTenderMatrixCell, match="kwota"):
        require_cell_amount("0")


_POSITIVE = st.decimals(
    min_value="0.0001",
    max_value="9999",
    places=4,
    allow_nan=False,
    allow_infinity=False,
)


@given(_POSITIVE)
def test_cell_amount_quantizes(units: Decimal) -> None:
    assert require_cell_amount(str(units)) == units


def test_cell_currency_iso() -> None:
    assert require_cell_currency("eur") == "EUR"


def test_cell_source_ref_accepts_fixture() -> None:
    assert (
        require_cell_source_ref(" fixture://tender-matrix-cell/1 ")
        == "fixture://tender-matrix-cell/1"
    )
    assert require_board_id(uuid4())


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_cell_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderMatrixCell, match="obce|wskazanie"):
        require_cell_source_ref(raw)
