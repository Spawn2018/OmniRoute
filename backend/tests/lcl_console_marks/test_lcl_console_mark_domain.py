import pytest

from app.domain.errors import InvalidLclConsoleMark
from app.domain.lcl_console_mark import parse_lcl_console_mark_row


def test_parse_lcl_console_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_lcl_console_mark_row(
        "lcm_console_01",
        "Console",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("lcm_console_01", "console", "tenant:manual")


def test_parse_lcl_console_mark_row_rejects_cbm_kind() -> None:
    with pytest.raises(InvalidLclConsoleMark, match="rodzaj"):
        parse_lcl_console_mark_row("lcm_console_01", "cbm", "tenant:manual")
