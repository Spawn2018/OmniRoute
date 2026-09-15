import pytest

from app.domain.errors import InvalidImpactNodeMark
from app.domain.impact_node_mark import parse_impact_node_mark_row


def _ok(**extra: object) -> tuple[str, str, str]:
    body: dict[str, object] = {
        "mark_code": "shipment_01",
        "node_kind": "shipment",
        "source_ref": "tenant:manual",
    }
    body.update(extra)
    return parse_impact_node_mark_row(
        body["mark_code"],
        body["node_kind"],
        body["source_ref"],
    )


def test_parse_accepts_shipment_kind() -> None:
    code, kind, origin = _ok()
    assert code == "shipment_01"
    assert kind == "shipment"
    assert origin == "tenant:manual"


@pytest.mark.parametrize(
    "token",
    ["inventory", "sku", "line", "order", "revenue", "margin", "cash", "other"],
)
def test_parse_accepts_all_node_kinds(token: str) -> None:
    _, kind, _ = _ok(node_kind=token)
    assert kind == token


def test_parse_rejects_bad_code() -> None:
    with pytest.raises(InvalidImpactNodeMark, match="oznaczenie"):
        _ok(mark_code="BAD")


def test_parse_rejects_unknown_kind() -> None:
    with pytest.raises(InvalidImpactNodeMark, match="rodzaj"):
        _ok(node_kind="direct")


def test_parse_rejects_bad_source_ref() -> None:
    with pytest.raises(InvalidImpactNodeMark, match="wskazanie"):
        _ok(source_ref="http://evil")
