import pytest

from app.domain.errors import InvalidOogPermitMark
from app.domain.oog_permit_mark import parse_oog_permit_mark_row


def test_parse_oog_permit_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_oog_permit_mark_row(
        "opm_permit_01",
        "Permit",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("opm_permit_01", "permit", "tenant:manual")


def test_parse_oog_permit_mark_row_rejects_metres_kind() -> None:
    with pytest.raises(InvalidOogPermitMark, match="rodzaj"):
        parse_oog_permit_mark_row("opm_permit_01", "metres", "tenant:manual")
