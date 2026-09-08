from uuid import uuid4

import pytest

from app.domain.errors import InvalidTenderLot
from app.domain.tender_lot import require_lot_code, require_lot_source_ref, require_tender_id


def test_lot_fields_accept_code_and_fixture() -> None:
    assert require_lot_code(" LOT-1 ") == "LOT-1"
    assert require_lot_source_ref(" fixture://tender-lot/1 ") == "fixture://tender-lot/1"
    assert require_tender_id(uuid4())


def test_lot_rejects_empty_code_and_foreign_ref() -> None:
    with pytest.raises(InvalidTenderLot, match="partia"):
        require_lot_code("  ")
    with pytest.raises(InvalidTenderLot, match="obce"):
        require_lot_source_ref("https://evil.example/lot")
