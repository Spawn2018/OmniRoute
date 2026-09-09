from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidPartyDocument
from app.domain.party_document import (
    require_document_kind,
    require_party_document_source_ref,
    require_party_id,
)


@given(st.sampled_from(["ocp", "ocs", "bdo_number"]))
def test_document_kind_normalizes_snake(raw: str) -> None:
    assert require_document_kind(raw) == raw


@given(st.sampled_from(["", "X", "SENT XML", "http://hold.example/x"]))
def test_document_kind_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidPartyDocument, match="dokument"):
        require_document_kind(raw)


def test_party_document_source_ref_accepts_fixture() -> None:
    assert require_party_document_source_ref(" fixture://party-document/1 ") == (
        "fixture://party-document/1"
    )
    assert require_party_id(uuid4())


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_party_document_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidPartyDocument, match="obce|wskazanie"):
        require_party_document_source_ref(raw)
