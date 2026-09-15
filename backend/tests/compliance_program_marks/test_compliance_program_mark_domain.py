import pytest

from app.domain.compliance_program_mark import parse_compliance_program_mark_row
from app.domain.errors import InvalidComplianceProgramMark


def test_parse_compliance_program_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_compliance_program_mark_row(
        "cp_draft_01",
        "Draft",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("cp_draft_01", "draft", "tenant:manual")


def test_parse_compliance_program_mark_row_rejects_score_kind() -> None:
    with pytest.raises(InvalidComplianceProgramMark, match="rodzaj"):
        parse_compliance_program_mark_row(
            "cp_draft_01",
            "auto_accept",
            "tenant:manual",
        )
