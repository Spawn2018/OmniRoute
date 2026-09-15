import pytest

from app.domain.crm_pipeline_mark import parse_crm_pipeline_mark_row
from app.domain.errors import InvalidCrmPipelineMark


def test_parse_crm_pipeline_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_crm_pipeline_mark_row(
        "crm_stage_01",
        "Stage",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("crm_stage_01", "stage", "tenant:manual")


def test_parse_crm_pipeline_mark_row_rejects_funnel_kind() -> None:
    with pytest.raises(InvalidCrmPipelineMark, match="rodzaj"):
        parse_crm_pipeline_mark_row("crm_stage_01", "funnel", "tenant:manual")
