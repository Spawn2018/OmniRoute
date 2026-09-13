import pytest

from app.domain.errors import InvalidTwinKind
from app.domain.twin_kind import parse_twin_kind_row


def _ok(**extra: object) -> object:
    body: dict[str, object] = {
        "kind_code": "tender",
        "source_ref": "tenant:manual",
    }
    body.update(extra)
    return parse_twin_kind_row(body["kind_code"], body["source_ref"])


def test_parse_accepts_open_kind_outside_mark_set() -> None:
    draft = _ok()
    assert draft.kind_code == "tender"


def test_parse_accepts_legacy_vehicle() -> None:
    draft = _ok(kind_code="vehicle")
    assert draft.kind_code == "vehicle"


def test_parse_rejects_bad_code() -> None:
    with pytest.raises(InvalidTwinKind, match="kod"):
        _ok(kind_code="X")


def test_parse_rejects_foreign_source() -> None:
    with pytest.raises(InvalidTwinKind, match="wskazanie"):
        _ok(source_ref="http://evil.example/x")
