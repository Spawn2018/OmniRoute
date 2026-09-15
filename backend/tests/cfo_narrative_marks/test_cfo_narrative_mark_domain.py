import pytest

from app.domain.cfo_narrative_mark import parse_cfo_narrative_mark_row
from app.domain.errors import InvalidCfoNarrativeMark


def test_parse_cfo_narrative_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_cfo_narrative_mark_row(
        "cfo_anomaly_01",
        "Anomaly",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("cfo_anomaly_01", "anomaly", "tenant:manual")


def test_parse_cfo_narrative_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidCfoNarrativeMark, match="rodzaj"):
        parse_cfo_narrative_mark_row(
            "cfo_anomaly_01",
            "auto_train",
            "tenant:manual",
        )
