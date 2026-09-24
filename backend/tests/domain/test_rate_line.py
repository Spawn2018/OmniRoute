from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidRateLine, InvalidSourceRef
from app.domain.rate_line import (
    require_allotment_teu,
    require_index_id,
    require_source_ref,
    require_spot_or_contract,
)

_ORIGIN = (
    st.text(min_size=1, max_size=512)
    .map(lambda text: text.strip())
    .filter(lambda text: 0 < len(text) <= 512)
)


def test_require_source_ref_strips_origin() -> None:
    assert require_source_ref(" tariff://msc-2026 ") == "tariff://msc-2026"


def test_require_source_ref_rejects_blank() -> None:
    with pytest.raises(InvalidSourceRef, match="obowiązkowy"):
        require_source_ref("   ")


def test_require_source_ref_rejects_non_text() -> None:
    with pytest.raises(InvalidSourceRef, match="tekstem"):
        require_source_ref(12)  # type: ignore[arg-type]


def test_require_source_ref_rejects_too_long() -> None:
    with pytest.raises(InvalidSourceRef, match="512"):
        require_source_ref("x" * 513)


@given(origin=_ORIGIN)
def test_require_source_ref_is_idempotent(origin: str) -> None:
    assert require_source_ref(origin) == origin
    assert require_source_ref(f" {origin} ") == origin


def test_require_allotment_teu_none_and_blank() -> None:
    assert require_allotment_teu(None) is None
    assert require_allotment_teu("") is None
    assert require_allotment_teu("  ") is None


def test_require_allotment_teu_quantizes() -> None:
    assert require_allotment_teu("12.5") == Decimal("12.5000")
    assert require_allotment_teu(Decimal("1")) == Decimal("1.0000")


def test_require_allotment_teu_rejects_negative() -> None:
    with pytest.raises(InvalidRateLine, match="ujemne"):
        require_allotment_teu("-1")


def test_require_allotment_teu_rejects_float() -> None:
    with pytest.raises(InvalidRateLine, match="float"):
        require_allotment_teu(1.5)  # type: ignore[arg-type]


def test_require_spot_or_contract_none_and_blank() -> None:
    assert require_spot_or_contract(None) is None
    assert require_spot_or_contract("") is None
    assert require_spot_or_contract("  ") is None


def test_require_spot_or_contract_normalizes() -> None:
    assert require_spot_or_contract(" Spot ") == "spot"
    assert require_spot_or_contract("CONTRACT") == "contract"
    assert require_spot_or_contract("other") == "other"


def test_require_spot_or_contract_rejects_unknown() -> None:
    with pytest.raises(InvalidRateLine, match="spot\\|contract\\|other"):
        require_spot_or_contract("futures")


def test_require_index_id_none_and_blank() -> None:
    assert require_index_id(None) is None
    assert require_index_id("") is None
    assert require_index_id("  ") is None


def test_require_index_id_trims() -> None:
    assert require_index_id(" FSC-Q3-2026 ") == "FSC-Q3-2026"


def test_require_index_id_rejects_too_long() -> None:
    with pytest.raises(InvalidRateLine, match="1–64"):
        require_index_id("x" * 65)


def test_require_index_id_rejects_non_string() -> None:
    with pytest.raises(InvalidRateLine, match="tekstem"):
        require_index_id(12)  # type: ignore[arg-type]
