from datetime import date
from uuid import uuid4

import pytest

from app.domain.errors import InvalidResource
from app.domain.resource_document import (
    parse_resource_document,
    require_document_kind,
    require_valid_until,
)


def test_document_kind_and_date() -> None:
    fleet = uuid4()
    parsed = parse_resource_document(str(fleet), "licence", "2027-01-15", "tenant:manual")
    assert parsed[0] == fleet
    assert parsed[1] == "licence"
    assert parsed[2] == date(2027, 1, 15)
    assert require_document_kind(" insurance ") == "insurance"
    assert require_valid_until("2026-12-31") == date(2026, 12, 31)


def test_rejects_unknown_kind_and_loose_date() -> None:
    with pytest.raises(InvalidResource, match="dokumentu"):
        require_document_kind("ocp")
    with pytest.raises(InvalidResource, match="ważność"):
        require_valid_until("15.01.2027")
    with pytest.raises(InvalidResource, match="ważność"):
        require_valid_until(20270115)
