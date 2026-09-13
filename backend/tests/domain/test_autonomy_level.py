import pytest

from app.domain.autonomy_level import parse_autonomy_level_row
from app.domain.errors import InvalidAutonomyLevel


def _ok(**extra: object) -> object:
    body: dict[str, object] = {
        "level_code": "observer",
        "source_ref": "tenant:manual",
    }
    body.update(extra)
    return parse_autonomy_level_row(body["level_code"], body["source_ref"])


def test_parse_accepts_open_level() -> None:
    draft = _ok()
    assert draft.level_code == "observer"


def test_parse_accepts_custom_outside_b4() -> None:
    draft = _ok(level_code="sales_desk")
    assert draft.level_code == "sales_desk"


def test_parse_rejects_bad_code() -> None:
    with pytest.raises(InvalidAutonomyLevel, match="kod"):
        _ok(level_code="X")


def test_parse_rejects_foreign_source() -> None:
    with pytest.raises(InvalidAutonomyLevel, match="wskazanie"):
        _ok(source_ref="http://evil.example/x")
