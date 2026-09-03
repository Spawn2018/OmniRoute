from uuid import uuid4

import pytest

from app.domain.errors import InvalidMailDraft, InvalidSourceRef
from app.domain.mail_draft import (
    mail_draft_extract_kind,
    mail_draft_status,
    require_mail_draft_body,
    require_mail_draft_source_ref,
    require_mail_draft_subject_id,
    require_mail_draft_subject_kind,
)


def test_draft_and_extract_constants() -> None:
    assert mail_draft_status() == "draft"
    assert mail_draft_extract_kind() == "extraction_draft"


def test_require_subject_kind_rejects_inbound() -> None:
    with pytest.raises(InvalidMailDraft, match="extraction_draft"):
        require_mail_draft_subject_kind("inbound_message")


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
