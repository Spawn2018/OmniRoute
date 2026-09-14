import pytest

from app.domain.errors import InvalidWmsFlowMark
from app.domain.wms_flow_mark import parse_wms_flow_mark_row


def test_parse_wms_flow_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_wms_flow_mark_row(
        "wms_receipt_01",
        "Receipt",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("wms_receipt_01", "receipt", "tenant:manual")


def test_parse_wms_flow_mark_row_rejects_live_wms_kind() -> None:
    with pytest.raises(InvalidWmsFlowMark, match="rodzaj"):
        parse_wms_flow_mark_row("wms_receipt_01", "live_wms", "tenant:manual")
