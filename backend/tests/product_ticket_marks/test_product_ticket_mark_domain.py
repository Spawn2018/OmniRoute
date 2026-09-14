import pytest

from app.domain.errors import InvalidProductTicketMark
from app.domain.product_ticket_mark import parse_product_ticket_mark_row


def test_parse_product_ticket_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_product_ticket_mark_row(
        "pt_report_01",
        "Report",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("pt_report_01", "report", "tenant:manual")


def test_parse_product_ticket_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidProductTicketMark, match="rodzaj"):
        parse_product_ticket_mark_row(
            "pt_report_01",
            "auto_fix",
            "tenant:manual",
        )
