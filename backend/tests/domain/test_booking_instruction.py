import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.booking_instruction import (
    require_booking_scope_token,
    require_instruction_status,
    require_instruction_target_role,
)
from app.domain.errors import InvalidBookingInstruction


def test_instruction_allowlists() -> None:
    assert require_booking_scope_token("contact_exchange") == "contact_exchange"
    assert require_instruction_target_role("origin_agent") == "origin_agent"
    assert require_instruction_status("suggested") == "suggested"


def test_instruction_rejects_ocean_booking_and_queued() -> None:
    with pytest.raises(InvalidBookingInstruction, match="zakres"):
        require_booking_scope_token("ocean_booking")
    with pytest.raises(InvalidBookingInstruction, match="status"):
        require_instruction_status("queued")
    with pytest.raises(InvalidBookingInstruction, match="rola"):
        require_instruction_target_role("sold_to")


@given(st.sampled_from(["queued", "draft", "http"]))
def test_instruction_status_rejects_foreign_tokens(raw: str) -> None:
    with pytest.raises(InvalidBookingInstruction, match="status"):
        require_instruction_status(raw)
