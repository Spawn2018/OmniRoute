from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidTenderTedNotice
from app.domain.tender_ted_notice import (
    require_board_id,
    require_notice_number,
    require_ted_source_ref,
)


@given(st.sampled_from(["123456-2024", "2024/S 012-000001"]))
def test_notice_number_keeps_operator_text(raw: str) -> None:
    assert require_notice_number(raw) == raw


@given(st.sampled_from(["", "TED", "http://ted.europa.eu/x", "abc"]))
def test_notice_number_rejects_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderTedNotice, match="ogłoszenie"):
        require_notice_number(raw)


def test_ted_source_ref_accepts_fixture() -> None:
    assert require_ted_source_ref(" fixture://tender-ted-notice/1 ") == (
        "fixture://tender-ted-notice/1"
    )
    assert require_board_id(uuid4())


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_ted_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidTenderTedNotice, match="obce|wskazanie"):
        require_ted_source_ref(raw)
