import pytest

from app.domain.errors import InvalidLineImpactLayerMark
from app.domain.line_impact_layer_mark import parse_line_impact_layer_mark_row


def test_parse_line_impact_layer_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_line_impact_layer_mark_row(
        "lil_scored_01",
        "Scored",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("lil_scored_01", "scored", "tenant:manual")


def test_parse_line_impact_layer_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidLineImpactLayerMark, match="rodzaj"):
        parse_line_impact_layer_mark_row(
            "lil_scored_01",
            "live_ebitda",
            "tenant:manual",
        )
