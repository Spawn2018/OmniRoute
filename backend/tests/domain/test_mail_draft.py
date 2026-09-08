from uuid import uuid4

import pytest

from app.domain.errors import InvalidMailDraft, InvalidSourceRef
from app.domain.mail_draft import (
    mail_draft_extract_kind,
    mail_draft_inquiry_kind,
    mail_draft_mailto_href,
    mail_draft_sent_status,
    mail_draft_status,
    require_mail_draft_body,
    require_mail_draft_source_ref,
    require_mail_draft_subject_id,
    require_mail_draft_subject_ids,
    require_mail_draft_subject_kind,
    require_mail_draft_to_address,
)


def test_draft_and_extract_constants() -> None:
    assert mail_draft_status() == "draft"
    assert mail_draft_sent_status() == "sent"
    assert mail_draft_extract_kind() == "extraction_draft"
    assert mail_draft_inquiry_kind() == "carrier_inquiry"


def test_require_subject_kind_rejects_inbound() -> None:
    with pytest.raises(InvalidMailDraft, match="allowlist"):
        require_mail_draft_subject_kind("inbound_message")


def test_require_subject_kind_accepts_inquiry() -> None:
    assert require_mail_draft_subject_kind("carrier_inquiry") == "carrier_inquiry"


def test_require_subject_ids_rejects_empty() -> None:
    with pytest.raises(InvalidMailDraft, match="batch"):
        require_mail_draft_subject_ids([])


def test_require_subject_id_rejects_non_uuid() -> None:
    with pytest.raises(InvalidMailDraft, match="UUID"):
        require_mail_draft_subject_id("not-a-uuid")  # type: ignore[arg-type]


def test_require_subject_id_passes_uuid() -> None:
    token = uuid4()
    assert require_mail_draft_subject_id(token) == token


def test_require_body_rejects_blank() -> None:
    with pytest.raises(InvalidMailDraft, match="obowiązkowa"):
        require_mail_draft_body("  ")


def test_require_source_ref_rejects_blank() -> None:
    with pytest.raises(InvalidSourceRef):
        require_mail_draft_source_ref("")


def test_require_to_address_normalizes() -> None:
    assert require_mail_draft_to_address("  Ops@Carrier.Example ") == "ops@carrier.example"


def test_require_to_address_rejects_blank() -> None:
    with pytest.raises(InvalidMailDraft, match="obowiązkowy"):
        require_mail_draft_to_address("  ")


def test_mailto_href_encodes_body() -> None:
    href = mail_draft_mailto_href("ops@carrier.example", "RFQ Gdynia")
    assert href.startswith("mailto:ops@carrier.example?body=")
    assert "RFQ" in href
