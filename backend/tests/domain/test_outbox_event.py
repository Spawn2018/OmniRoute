from uuid import uuid4

import pytest

from app.domain.errors import InvalidOutboxEvent, InvalidSourceRef
from app.domain.outbox_event import (
    inbound_message_saved_kind,
    outbox_pending_status,
    require_outbox_event_kind,
    require_outbox_source_ref,
    require_outbox_subject_id,
    task_template_saved_kind,
)


def test_outbox_pending_status_is_pending() -> None:
    assert outbox_pending_status() == "pending"


def test_inbound_message_saved_kind() -> None:
    assert inbound_message_saved_kind() == "inbound_message_saved"


def test_task_template_saved_kind() -> None:
    assert task_template_saved_kind() == "task_template_saved"


def test_require_outbox_event_kind_accepts_both() -> None:
    assert require_outbox_event_kind("inbound_message_saved") == "inbound_message_saved"
    assert require_outbox_event_kind("task_template_saved") == "task_template_saved"


def test_require_outbox_source_ref_accepts_prefix() -> None:
    assert require_outbox_source_ref(" outbox://inbound-message/1 ") == (
        "outbox://inbound-message/1"
    )


def test_require_outbox_source_ref_rejects_fixture() -> None:
    with pytest.raises(InvalidOutboxEvent, match="outbox://"):
        require_outbox_source_ref("fixture://mail/1")


def test_require_outbox_source_ref_rejects_blank() -> None:
    with pytest.raises(InvalidSourceRef, match="obowiązkowy"):
        require_outbox_source_ref("  ")


def test_require_outbox_event_kind_rejects_other() -> None:
    with pytest.raises(InvalidOutboxEvent, match="inbound_message_saved"):
        require_outbox_event_kind("processed")


def test_require_outbox_subject_id_accepts_uuid() -> None:
    token = uuid4()
    assert require_outbox_subject_id(token) == token
    assert require_outbox_subject_id(str(token)) == token


def test_require_outbox_subject_id_rejects_text() -> None:
    with pytest.raises(InvalidOutboxEvent, match="UUID"):
        require_outbox_subject_id("not-a-uuid")
