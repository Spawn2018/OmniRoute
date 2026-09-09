from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidKreptdLicence
from app.domain.kreptd_licence import (
    require_kreptd_source_ref,
    require_licence_no,
    require_party_id,
)


@given(st.sampled_from(["GITD-12345678", "12345678"]))
def test_licence_no_keeps_operator_text(raw: str) -> None:
    assert require_licence_no(raw) == raw


@given(st.sampled_from(["", "LICENCE", "http://kreptd.gitd.gov.pl/x", "abcdefg"]))
def test_licence_no_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidKreptdLicence, match="licencja"):
        require_licence_no(raw)


def test_kreptd_source_ref_accepts_fixture() -> None:
    assert require_kreptd_source_ref(" fixture://kreptd-licence/1 ") == (
        "fixture://kreptd-licence/1"
    )
    assert require_party_id(uuid4())


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_kreptd_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidKreptdLicence, match="obce|wskazanie"):
        require_kreptd_source_ref(raw)
