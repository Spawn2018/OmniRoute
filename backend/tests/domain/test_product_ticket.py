import pytest

from app.domain.errors import InvalidProductTicket
from app.domain.product_ticket import parse_product_ticket_row


def test_parse_product_ticket_accepts_manual() -> None:
    code, title, body, kind, origin = parse_product_ticket_row(
        " bug_login_01 ",
        " Login stuck ",
        " Cannot enter ",
        " REPORT ",
        " tenant:manual ",
    )
    assert code == "bug_login_01"
    assert title == "Login stuck"
    assert body == "Cannot enter"
    assert kind == "report"
    assert origin == "tenant:manual"


def test_parse_product_ticket_rejects_blank_title() -> None:
    with pytest.raises(InvalidProductTicket, match="tytuł"):
        parse_product_ticket_row(
            "bug_login_01",
            "  ",
            "body",
            "report",
            "tenant:manual",
        )


def test_parse_product_ticket_rejects_unknown_kind() -> None:
    with pytest.raises(InvalidProductTicket, match="rodzaj"):
        parse_product_ticket_row(
            "bug_login_01",
            "title",
            "body",
            "closed",
            "tenant:manual",
        )
