from uuid import uuid4

import pytest

from app.domain.errors import InvalidOperatorDecision, InvalidSourceRef
from app.domain.operator_decision import (
    next_lock_version,
    operator_decision_pending_status,
    require_decide_status,
    require_decision_source_ref,
    require_lock_version,
    require_pending_before_decide,
    require_subject_id,
    require_subject_kind,
)


def test_pending_status_is_pending() -> None:
    assert operator_decision_pending_status() == "pending"


def test_require_subject_kind_accepts_inbound_message() -> None:
    assert require_subject_kind(" inbound_message ") == "inbound_message"


def test_require_subject_kind_accepts_mail_draft() -> None:
    assert require_subject_kind("mail_draft") == "mail_draft"


def test_require_subject_kind_rejects_other() -> None:
    with pytest.raises(InvalidOperatorDecision, match="mail_draft"):
        require_subject_kind("quotation")


def test_require_subject_id_rejects_non_uuid() -> None:
    with pytest.raises(InvalidOperatorDecision, match="UUID"):
        require_subject_id("not-a-uuid")  # type: ignore[arg-type]


def test_require_subject_id_passes_uuid() -> None:
    token = uuid4()
    assert require_subject_id(token) == token


def test_require_decide_status_accepts_accept_or_reject() -> None:
    assert require_decide_status("accepted") == "accepted"
    assert require_decide_status(" rejected ") == "rejected"


def test_require_decide_status_rejects_changed() -> None:
    with pytest.raises(InvalidOperatorDecision, match="accepted"):
        require_decide_status("changed")


def test_require_pending_before_decide_rejects_second_write() -> None:
    with pytest.raises(InvalidOperatorDecision, match="już zapisana"):
        require_pending_before_decide("accepted")


def test_require_decision_source_ref_rejects_blank() -> None:
    with pytest.raises(InvalidSourceRef):
        require_decision_source_ref("  ")


def test_require_lock_version_rejects_negative() -> None:
    with pytest.raises(InvalidOperatorDecision, match="ujemny"):
        require_lock_version(-1)


def test_next_lock_version_increments() -> None:
    assert next_lock_version(0) == 1
