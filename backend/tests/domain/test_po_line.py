from decimal import Decimal
from uuid import uuid4

import pytest

from app.domain.errors import InvalidPoLine
from app.domain.po_line import parse_po_line_row


def _parse(**overrides: object) -> tuple[object, ...]:
    body: dict[str, object] = {
        "purchase_order_id": uuid4(),
        "line_code": "line_01",
        "sku_code": "SKU-4401",
        "qty": "12.5",
        "uom_code": "pcs",
        "plant_label": "Gdańsk",
        "batch_label": "B-1",
        "serial_label": "S-9",
        "coo_label": "PL",
        "source_ref": "tenant:manual",
    }
    body.update(overrides)
    return parse_po_line_row(**body)


def test_parse_po_line_row_accepts_decimal_string_and_labels() -> None:
    header = uuid4()
    packed = parse_po_line_row(
        purchase_order_id=header,
        line_code="line_01",
        sku_code=" SKU-4401 ",
        qty="12.5",
        uom_code=" pcs ",
        plant_label=" Gdańsk ",
        batch_label=" B-1 ",
        serial_label=" S-9 ",
        coo_label=" PL ",
        source_ref="fixture://po-line/a",
    )
    assert packed[0] == header
    assert packed[1] == "line_01"
    assert packed[2] == "SKU-4401"
    assert packed[3] == Decimal("12.5000")
    assert packed[4] == "pcs"
    assert packed[5] == "Gdańsk"
    assert packed[6] == "B-1"
    assert packed[7] == "S-9"
    assert packed[8] == "PL"
    assert packed[9] == "fixture://po-line/a"


def test_parse_po_line_row_accepts_zero_qty_and_blank_labels() -> None:
    packed = _parse(qty=0, plant_label="  ", batch_label=None, serial_label="", coo_label=None)
    assert packed[3] == Decimal("0.0000")
    assert packed[5] is None
    assert packed[6] is None
    assert packed[7] is None
    assert packed[8] is None


def test_parse_po_line_row_rejects_bad_line_code() -> None:
    with pytest.raises(InvalidPoLine, match="linia"):
        _parse(line_code="X")
    with pytest.raises(InvalidPoLine, match="linia"):
        _parse(line_code=1)


def test_parse_po_line_row_rejects_float_qty() -> None:
    with pytest.raises(InvalidPoLine, match="ilość"):
        _parse(qty=1.5)
    with pytest.raises(InvalidPoLine, match="ilość"):
        _parse(qty=True)
    with pytest.raises(InvalidPoLine, match="ilość"):
        _parse(qty="-1")


def test_parse_po_line_row_rejects_bad_sku_uom_and_origin() -> None:
    with pytest.raises(InvalidPoLine, match="sku"):
        _parse(sku_code="")
    with pytest.raises(InvalidPoLine, match="jm"):
        _parse(uom_code="")
    with pytest.raises(InvalidPoLine, match="obce"):
        _parse(source_ref="https://vendor.example/asn")
