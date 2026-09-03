from uuid import uuid4

import pytest

from app.domain.carrier_inquiry import (
    carrier_inquiry_draft_status,
    carrier_inquiry_manual_source,
    require_network_member_id,
)
from app.domain.errors import InvalidCarrierInquiry


def test_carrier_inquiry_draft_is_draft() -> None:
    assert carrier_inquiry_draft_status() == "draft"


def test_carrier_inquiry_source_is_manual() -> None:
    assert carrier_inquiry_manual_source() == "tenant:manual"


def test_require_network_member_id_rejects_text() -> None:
    with pytest.raises(InvalidCarrierInquiry, match="UUID"):
        require_network_member_id("agent")  # type: ignore[arg-type]


def test_require_network_member_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_network_member_id(token) == token
