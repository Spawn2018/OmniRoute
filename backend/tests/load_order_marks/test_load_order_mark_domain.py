import pytest

from app.domain.errors import InvalidLoadOrderMark
from app.domain.load_order_mark import parse_load_order_mark_row


def test_parse_load_order_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_load_order_mark_row(
        "lor_seq_01",
        "Sequence",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("lor_seq_01", "sequence", "tenant:manual")


def test_parse_load_order_mark_row_rejects_solver_kind() -> None:
    with pytest.raises(InvalidLoadOrderMark, match="rodzaj"):
        parse_load_order_mark_row("lor_seq_01", "solver", "tenant:manual")
