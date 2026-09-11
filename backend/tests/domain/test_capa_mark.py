import pytest

from app.domain.capa_mark import parse_capa_mark_row
from app.domain.errors import InvalidCapaMark


def test_parse_capa_mark_row_accepts() -> None:
    code, kind, origin = parse_capa_mark_row(
        " capa_pl_01 ", " Capa ", "fixture://capa-mark/a"
    )
    assert code == "capa_pl_01"
    assert kind == "capa"
    assert origin == "fixture://capa-mark/a"


def test_parse_capa_mark_row_rejects() -> None:
    with pytest.raises(InvalidCapaMark, match="oznaczenie"):
        parse_capa_mark_row("X", "capa", "tenant:manual")
    with pytest.raises(InvalidCapaMark, match="rodzaj"):
        parse_capa_mark_row("capa_01", "workflow", "tenant:manual")
    with pytest.raises(InvalidCapaMark, match="obce"):
        parse_capa_mark_row("capa_01", "eight_d", "http://evil")
