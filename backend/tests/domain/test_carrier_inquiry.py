from datetime import date
from uuid import uuid4

import pytest

from app.domain.carrier_inquiry import (
    carrier_inquiry_draft_status,
    carrier_inquiry_manual_source,
    require_answered_quote,
    require_inquiry_status,
    require_member_batch,
    require_network_member_id,
    require_no_reply_after,
    require_silent_filter,
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


def test_inquiry_status_rejects_unknown() -> None:
    with pytest.raises(InvalidCarrierInquiry, match="allowlisty"):
        require_inquiry_status("flying")
    assert require_inquiry_status("queued") == "queued"


def test_answered_quote_rejected_on_draft() -> None:
    with pytest.raises(InvalidCarrierInquiry, match="answered"):
        require_answered_quote(
            status="draft",
            quoted_amount="10",
            quoted_currency="USD",
            quoted_transit_days=None,
        )


def test_member_batch_rejects_empty() -> None:
    with pytest.raises(InvalidCarrierInquiry, match="listy"):
        require_member_batch([])
    token = uuid4()
    assert require_member_batch([token]) == [token]


def test_no_reply_after_accepts_iso_or_blank() -> None:
    assert require_no_reply_after(None) is None
    assert require_no_reply_after("  ") is None
    assert require_no_reply_after("2026-09-01") == date(2026, 9, 1)
    with pytest.raises(InvalidCarrierInquiry, match="kalendarzowa"):
        require_no_reply_after("poniedzialek")


def test_silent_filter_only_overdue() -> None:
    assert require_silent_filter(None) is None
    assert require_silent_filter("overdue") == "overdue"
    with pytest.raises(InvalidCarrierInquiry, match="overdue"):
        require_silent_filter("thread")
