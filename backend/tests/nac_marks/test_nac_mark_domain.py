import pytest

from app.domain.errors import InvalidNacMark
from app.domain.nac_mark import parse_nac_mark_row


def test_parse_nac_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_nac_mark_row(
        "nac_agent_01",
        "Agent",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("nac_agent_01", "agent", "tenant:manual")


def test_parse_nac_mark_row_rejects_live_http_kind() -> None:
    with pytest.raises(InvalidNacMark, match="rodzaj"):
        parse_nac_mark_row("nac_agent_01", "live_http", "tenant:manual")
