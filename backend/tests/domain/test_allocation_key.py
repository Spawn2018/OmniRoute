import pytest

from app.domain.allocation_key import parse_allocation_key_row
from app.domain.errors import InvalidAllocationKey


def _ok(**extra: object) -> object:
    body: dict[str, object] = {
        "key_code": "lane_direct",
        "source_ref": "tenant:manual",
    }
    body.update(extra)
    return parse_allocation_key_row(body["key_code"], body["source_ref"])


def test_parse_accepts_open_key() -> None:
    draft = _ok()
    assert draft.key_code == "lane_direct"


def test_parse_accepts_custom_outside_list() -> None:
    draft = _ok(key_code="shared_yard")
    assert draft.key_code == "shared_yard"


def test_parse_rejects_bad_code() -> None:
    with pytest.raises(InvalidAllocationKey, match="kod"):
        _ok(key_code="X")


def test_parse_rejects_foreign_source() -> None:
    with pytest.raises(InvalidAllocationKey, match="wskazanie"):
        _ok(source_ref="http://evil.example/x")
