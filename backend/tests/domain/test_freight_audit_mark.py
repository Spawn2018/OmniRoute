import pytest

from app.domain.errors import InvalidFreightAuditMark
from app.domain.freight_audit_mark import parse_freight_audit_mark_row


def test_parse_freight_audit_accepts() -> None:
    code, kind, origin = parse_freight_audit_mark_row(
        " audit_inv_01 ",
        " Expected_Vs_Invoice ",
        "fixture://freight-audit-mark/a",
    )
    assert code == "audit_inv_01"
    assert kind == "expected_vs_invoice"
    assert origin == "fixture://freight-audit-mark/a"


def test_parse_freight_audit_rejects() -> None:
    with pytest.raises(InvalidFreightAuditMark, match="oznaczenie"):
        parse_freight_audit_mark_row("X", "expected_vs_invoice", "tenant:manual")
    with pytest.raises(InvalidFreightAuditMark, match="rodzaj"):
        parse_freight_audit_mark_row("audit_01", "margin_delta", "tenant:manual")
    with pytest.raises(InvalidFreightAuditMark, match="obce"):
        parse_freight_audit_mark_row("audit_01", "expected_vs_charge", "http://evil")
