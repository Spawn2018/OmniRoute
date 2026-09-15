import pytest

from app.domain.allocation_level import parse_allocation_level_row
from app.domain.errors import InvalidAllocationLevel


def _ok(**extra: object) -> object:
    body: dict[str, object] = {
        "level_code": "tier_one",
        "source_ref": "tenant:manual",
    }
    body.update(extra)
    return parse_allocation_level_row(body["level_code"], body["source_ref"])


def test_parse_accepts_open_key() -> None:
    draft = _ok()
    assert draft.level_code == "tier_one"


def test_parse_accepts_custom_outside_list() -> None:
    draft = _ok(level_code="tier_two")
    assert draft.level_code == "tier_two"


def test_parse_rejects_bad_code() -> None:
    with pytest.raises(InvalidAllocationLevel, match="kod"):
        _ok(level_code="X")


def test_parse_rejects_foreign_source() -> None:
    with pytest.raises(InvalidAllocationLevel, match="wskazanie"):
        _ok(source_ref="http://evil.example/x")
