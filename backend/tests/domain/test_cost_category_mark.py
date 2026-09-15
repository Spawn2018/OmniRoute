import pytest

from app.domain.cost_category_mark import parse_cost_category_mark_row
from app.domain.errors import InvalidCostCategoryMark


def _ok(**extra: object) -> tuple[str, str, str]:
    body: dict[str, object] = {
        "mark_code": "direct_01",
        "category_kind": "direct",
        "source_ref": "tenant:manual",
    }
    body.update(extra)
    return parse_cost_category_mark_row(
        body["mark_code"],
        body["category_kind"],
        body["source_ref"],
    )


def test_parse_accepts_direct_kind() -> None:
    code, kind, origin = _ok()
    assert code == "direct_01"
    assert kind == "direct"
    assert origin == "tenant:manual"


@pytest.mark.parametrize(
    "token",
    ["shared", "allocated", "overhead", "capital", "risk", "other"],
)
def test_parse_accepts_all_category_kinds(token: str) -> None:
    _, kind, _ = _ok(category_kind=token)
    assert kind == token


def test_parse_rejects_bad_code() -> None:
    with pytest.raises(InvalidCostCategoryMark, match="oznaczenie"):
        _ok(mark_code="BAD")


def test_parse_rejects_bad_kind() -> None:
    with pytest.raises(InvalidCostCategoryMark, match="rodzaj"):
        _ok(category_kind="engine")


def test_parse_rejects_foreign_source() -> None:
    with pytest.raises(InvalidCostCategoryMark, match="wskazanie"):
        _ok(source_ref="http://evil.example/x")
