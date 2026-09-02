from uuid import uuid4

import pytest

from app.domain.customer_rfq import (
    customer_rfq_draft_status,
    require_inbound_message_id,
    require_rfq_source_ref,
)
from app.domain.errors import InvalidCustomerRfq, InvalidInboundMessage


def test_customer_rfq_draft_status_is_draft() -> None:
    assert customer_rfq_draft_status() == "draft"


def test_require_rfq_source_ref_accepts_fixture() -> None:
    assert require_rfq_source_ref(" fixture://inbound-mail/1 ") == "fixture://inbound-mail/1"


def test_require_rfq_source_ref_rejects_imap() -> None:
    with pytest.raises(InvalidInboundMessage, match="fixture"):
        require_rfq_source_ref("imap://inbox")


def test_require_inbound_message_id_rejects_non_uuid() -> None:
    with pytest.raises(InvalidCustomerRfq, match="UUID"):
        require_inbound_message_id("not-a-uuid")  # type: ignore[arg-type]


def test_require_inbound_message_id_passes_uuid() -> None:
    token = uuid4()
    assert require_inbound_message_id(token) == token
