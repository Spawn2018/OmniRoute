import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidSourceRef
from app.domain.rate_line import require_source_ref

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
