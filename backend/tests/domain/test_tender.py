from datetime import date
from uuid import uuid4

import pytest

from app.domain.errors import InvalidTender
from app.domain.tender import (
    require_board_source_ref,
    require_buyer_id,
    require_deadline_at,
    require_incoterm,
    require_kind,
    require_named_place,
    require_side,
    require_status,
    require_trade_side,
)


def test_board_fields_accept_sell_open_draft() -> None:
    assert require_side(" sell ") == "sell"
    assert require_kind("open") == "open"
    assert require_status("draft") == "draft"
    assert require_deadline_at("2026-12-31") == date(2026, 12, 31)
    assert require_incoterm("fob") == "FOB"
    assert require_trade_side("export") == "export"
    assert require_named_place("FOB", " Gdynia ") == "Gdynia"
    assert require_board_source_ref(" fixture://tender/1 ") == "fixture://tender/1"
    assert require_buyer_id(uuid4())


def test_board_rejects_bad_side_kind_status_and_foreign_ref() -> None:
    with pytest.raises(InvalidTender, match="strona"):
        require_side("both")
    with pytest.raises(InvalidTender, match="rodzaj"):
        require_kind("silent")
    with pytest.raises(InvalidTender, match="status"):
        require_status("auto")
    with pytest.raises(InvalidTender, match="termin"):
        require_deadline_at("31-12-2026")
    with pytest.raises(InvalidTender, match="incoterm"):
        require_incoterm("XXX")
    with pytest.raises(InvalidTender, match="miejsce"):
        require_named_place("DAP", "")
    with pytest.raises(InvalidTender, match="obce"):
        require_board_source_ref("https://evil.example/tender")
