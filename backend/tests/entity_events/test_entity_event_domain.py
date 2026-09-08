from uuid import uuid4

import pytest

from app.domain.entity_event import (
    require_entity_event_kind,
    require_entity_source_ref,
    require_entity_subject_id,
    require_entity_subject_kind,
)
from app.domain.errors import InvalidEntityEvent, InvalidSourceRef


def test_allowlisted_kinds_pass() -> None:
    assert require_entity_event_kind("inquiry_queued") == "inquiry_queued"
    assert require_entity_event_kind("inquiry_sent") == "inquiry_sent"
    assert require_entity_event_kind("quote_recorded") == "quote_recorded"
    assert require_entity_subject_kind("carrier_inquiry") == "carrier_inquiry"
    assert require_entity_subject_kind("quotation") == "quotation"
    assert require_entity_subject_kind("channel_quote") == "channel_quote"


def test_kind_outside_allowlist_is_rejected() -> None:
    with pytest.raises(InvalidEntityEvent, match="event_kind"):
        require_entity_event_kind("prediction_scored")
    with pytest.raises(InvalidEntityEvent, match="subject_kind"):
        require_entity_subject_kind("outbox_event")


def test_source_ref_is_required() -> None:
    with pytest.raises(InvalidSourceRef):
        require_entity_source_ref("")
    assert require_entity_source_ref("entity://inquiry/1") == "entity://inquiry/1"


def test_subject_id_must_be_uuid() -> None:
    token = uuid4()
    assert require_entity_subject_id(token) == token
    with pytest.raises(InvalidEntityEvent, match="UUID"):
        require_entity_subject_id("nie-uuid")
