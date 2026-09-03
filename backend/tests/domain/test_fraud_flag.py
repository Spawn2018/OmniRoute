from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidFraudFlag
from app.domain.fraud_flag import (
    require_flag_kind,
    require_flag_party_id,
    require_flag_source_ref,
)


def test_require_flag_kind_accepts_allowlist() -> None:
    assert require_flag_kind(" billing ") == "billing"
    assert require_flag_kind("document") == "document"
    assert require_flag_kind("other") == "other"


def test_require_flag_kind_rejects_unknown() -> None:
    with pytest.raises(InvalidFraudFlag, match="rodzaj"):
        require_flag_kind("score")


def test_require_flag_source_ref_accepts_fixture() -> None:
    assert require_flag_source_ref(" fixture://fraud-flag/1 ") == "fixture://fraud-flag/1"


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_flag_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidFraudFlag):
        require_flag_source_ref(raw)


def test_require_flag_party_id_rejects_text() -> None:
    with pytest.raises(InvalidFraudFlag, match="UUID"):
        require_flag_party_id("flag")  # type: ignore[arg-type]


def test_require_flag_party_id_keeps_uuid() -> None:
    token = uuid4()
    assert require_flag_party_id(token) == token
