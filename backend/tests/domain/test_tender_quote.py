from datetime import date
from uuid import uuid4

import pytest

from app.domain.errors import InvalidTenderQuote
from app.domain.tender_quote import (
    require_bid_source_ref,
    require_order_limit,
    require_quote_id,
    require_valid_until,
)


def test_bid_fields_accept_iso_and_positive_limit() -> None:
    assert require_valid_until("2026-12-31") == date(2026, 12, 31)
    assert require_order_limit(3) == 3
    assert require_bid_source_ref(" fixture://tender-quote/1 ") == "fixture://tender-quote/1"
    assert require_quote_id(uuid4())


def test_bid_rejects_bad_date_limit_and_foreign_ref() -> None:
    with pytest.raises(InvalidTenderQuote, match="data"):
        require_valid_until("31-12-2026")
    with pytest.raises(InvalidTenderQuote, match="limit"):
        require_order_limit(0)
    with pytest.raises(InvalidTenderQuote, match="limit"):
        require_order_limit(1.5)  # type: ignore[arg-type]
    with pytest.raises(InvalidTenderQuote, match="obce"):
        require_bid_source_ref("https://evil.example/tender")
