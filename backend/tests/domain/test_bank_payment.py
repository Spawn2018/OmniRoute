from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.bank_payment import (
    require_payment_account_id,
    require_payment_invoice_id,
    require_payment_source_ref,
)
from app.domain.errors import InvalidBankPayment


def test_require_payment_source_ref_accepts_fixture() -> None:
    assert (
        require_payment_source_ref(" fixture://bank-payment/1 ") == "fixture://bank-payment/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_require_payment_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidBankPayment):
        require_payment_source_ref(raw)


def test_require_payment_ids_keep_uuid() -> None:
    token = uuid4()
    assert require_payment_invoice_id(token) == token
    assert require_payment_account_id(token) == token


def test_require_payment_ids_reject_text() -> None:
    with pytest.raises(InvalidBankPayment, match="UUID"):
        require_payment_invoice_id("i")  # type: ignore[arg-type]
    with pytest.raises(InvalidBankPayment, match="UUID"):
        require_payment_account_id("a")  # type: ignore[arg-type]
