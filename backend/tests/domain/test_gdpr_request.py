from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidGdprRequest
from app.domain.gdpr_request import (
    ERASED_DISPLAY_NAME,
    erasure_mailbox,
    require_gdpr_app_user_id,
    require_gdpr_request_kind,
    require_gdpr_request_source_ref,
    require_open_gdpr_request,
)


def test_require_gdpr_request_source_ref_accepts_fixture() -> None:
    assert (
        require_gdpr_request_source_ref(" fixture://gdpr-request/1 ")
        == "fixture://gdpr-request/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_gdpr_request_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidGdprRequest):
        require_gdpr_request_source_ref(raw)


def test_require_gdpr_request_kind_keeps_access_and_erasure() -> None:
    assert require_gdpr_request_kind("access") == "access"
    assert require_gdpr_request_kind("erasure") == "erasure"


@given(st.sampled_from(["export", "delete", "ACCESS", ""]))
def test_require_gdpr_request_kind_rejects_unknown(raw: str) -> None:
    with pytest.raises(InvalidGdprRequest):
        require_gdpr_request_kind(raw)


def test_require_gdpr_app_user_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_gdpr_app_user_id(token) == token


def test_require_gdpr_app_user_id_rejects_text() -> None:
    with pytest.raises(InvalidGdprRequest, match="UUID"):
        require_gdpr_app_user_id("u")  # type: ignore[arg-type]


def test_erasure_mailbox_uses_user_hex_and_invalid_tld() -> None:
    token = uuid4()
    assert erasure_mailbox(token) == f"erased.{token.hex}@erased.invalid"
    assert ERASED_DISPLAY_NAME == "usunięte"


def test_require_open_gdpr_request_rejects_fulfilled() -> None:
    with pytest.raises(InvalidGdprRequest, match="wypełniony"):
        require_open_gdpr_request("fulfilled")
