import pytest

from app.domain.errors import InvalidImpactEdgeMark
from app.domain.impact_edge_mark import parse_impact_edge_mark_row


def _ok(**extra: object) -> tuple[str, str, str, str]:
    body: dict[str, object] = {
        "mark_code": "ship_to_inv",
        "from_kind": "shipment",
        "to_kind": "inventory",
        "source_ref": "tenant:manual",
    }
    body.update(extra)
    return parse_impact_edge_mark_row(
        body["mark_code"],
        body["from_kind"],
        body["to_kind"],
        body["source_ref"],
    )


def test_parse_accepts_shipment_to_inventory() -> None:
    code, start, end, origin = _ok()
    assert code == "ship_to_inv"
    assert start == "shipment"
    assert end == "inventory"
    assert origin == "tenant:manual"


@pytest.mark.parametrize(
    "token",
    ["inventory", "sku", "line", "order", "revenue", "margin", "cash", "other"],
)
def test_parse_accepts_all_kinds_as_from(token: str) -> None:
    _, start, _, _ = _ok(from_kind=token)
    assert start == token


@pytest.mark.parametrize(
    "token",
    ["shipment", "sku", "line", "order", "revenue", "margin", "cash", "other"],
)
def test_parse_accepts_all_kinds_as_to(token: str) -> None:
    _, _, end, _ = _ok(to_kind=token)
    assert end == token


def test_parse_rejects_bad_code() -> None:
    with pytest.raises(InvalidImpactEdgeMark, match="oznaczenie"):
        _ok(mark_code="BAD")


def test_parse_rejects_unknown_from_kind() -> None:
    with pytest.raises(InvalidImpactEdgeMark, match="from_kind"):
        _ok(from_kind="engine")


def test_parse_rejects_unknown_to_kind() -> None:
    with pytest.raises(InvalidImpactEdgeMark, match="to_kind"):
        _ok(to_kind="engine")


def test_parse_rejects_bad_source_ref() -> None:
    with pytest.raises(InvalidImpactEdgeMark, match="wskazanie"):
        _ok(source_ref="http://evil")
