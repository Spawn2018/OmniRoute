import pytest

from app.domain.errors import InvalidGroupageDispatcherMark
from app.domain.groupage_dispatcher_mark import parse_groupage_dispatcher_mark_row


def test_parse_groupage_dispatcher_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_groupage_dispatcher_mark_row(
        "gdp_line_01",
        "Line",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("gdp_line_01", "line", "tenant:manual")


def test_parse_groupage_dispatcher_mark_row_rejects_engine_kind() -> None:
    with pytest.raises(InvalidGroupageDispatcherMark, match="rodzaj"):
        parse_groupage_dispatcher_mark_row("gdp_line_01", "engine", "tenant:manual")
