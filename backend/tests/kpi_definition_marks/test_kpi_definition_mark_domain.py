import pytest

from app.domain.errors import InvalidKpiDefinitionMark
from app.domain.kpi_definition_mark import parse_kpi_definition_mark_row


def test_parse_kpi_definition_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_kpi_definition_mark_row(
        "kpi_otd_01",
        "Otd",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("kpi_otd_01", "otd", "tenant:manual")


def test_parse_kpi_definition_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidKpiDefinitionMark, match="rodzaj"):
        parse_kpi_definition_mark_row(
            "kpi_otd_01",
            "llm_formula",
            "tenant:manual",
        )
