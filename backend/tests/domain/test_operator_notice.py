import pytest

from app.domain.errors import InvalidOperatorNotice, InvalidSourceRef
from app.domain.operator_notice import (
    notice_after_read,
    operator_notice_manual_kind,
    operator_notice_no_reply_kind,
    operator_notice_unread_status,
    require_notice_body,
    require_notice_kind,
    require_notice_source_ref,
)


def test_unread_and_manual_constants() -> None:
    assert operator_notice_unread_status() == "unread"
    assert operator_notice_manual_kind() == "manual"
    assert operator_notice_no_reply_kind() == "no_reply"


def test_require_notice_kind_rejects_quote_filter() -> None:
    with pytest.raises(InvalidOperatorNotice, match="allowlisty"):
        require_notice_kind("offer_acceptance")
    assert require_notice_kind("no_reply") == "no_reply"


def test_require_notice_body_rejects_blank() -> None:
    with pytest.raises(InvalidOperatorNotice, match="obowiązkowa"):
        require_notice_body("  ")


def test_require_notice_source_ref_rejects_blank() -> None:
    with pytest.raises(InvalidSourceRef):
        require_notice_source_ref("")


def test_notice_after_read_is_idempotent() -> None:
    assert notice_after_read("unread") == "read"
    assert notice_after_read("read") == "read"
