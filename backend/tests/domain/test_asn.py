from uuid import uuid4

import pytest

from app.domain.asn import parse_asn_row
from app.domain.errors import InvalidAsn


def _parse(**overrides: object) -> tuple[object, ...]:
    body: dict[str, object] = {
        "purchase_order_id": uuid4(),
        "asn_code": "asn_01",
        "plant_label": "Gdańsk",
        "carrier_label": "DB Schenker",
        "ship_ref_label": "REF-9",
        "guide_code": None,
        "source_ref": "tenant:manual",
    }
    body.update(overrides)
    return parse_asn_row(**body)


def test_parse_asn_row_accepts_code_and_labels() -> None:
    header = uuid4()
    packed = parse_asn_row(
        purchase_order_id=header,
        asn_code=" asn_01 ",
        plant_label=" Gdańsk ",
        carrier_label=" DB Schenker ",
        ship_ref_label=" REF-9 ",
        guide_code=" lane_pl_de ",
        source_ref="fixture://asn/a",
    )
    assert packed[0] == header
    assert packed[1] == "asn_01"
    assert packed[2] == "Gdańsk"
    assert packed[3] == "DB Schenker"
    assert packed[4] == "REF-9"
    assert packed[5] == "lane_pl_de"
    assert packed[6] == "fixture://asn/a"


def test_parse_asn_row_accepts_blank_labels() -> None:
    packed = _parse(plant_label="  ", carrier_label=None, ship_ref_label="", guide_code="")
    assert packed[2] is None
    assert packed[3] is None
    assert packed[4] is None
    assert packed[5] is None


def test_parse_asn_row_rejects_bad_asn_code() -> None:
    with pytest.raises(InvalidAsn, match="awizo"):
        _parse(asn_code="X")
    with pytest.raises(InvalidAsn, match="awizo"):
        _parse(asn_code=1)


def test_parse_asn_row_rejects_bad_guide_code() -> None:
    with pytest.raises(InvalidAsn, match="przewodnik"):
        _parse(guide_code="X")
    with pytest.raises(InvalidAsn, match="przewodnik"):
        _parse(guide_code=1)


def test_parse_asn_row_rejects_bad_labels_and_origin() -> None:
    with pytest.raises(InvalidAsn, match="zakład"):
        _parse(plant_label=1)
    with pytest.raises(InvalidAsn, match="przewoźnik"):
        _parse(carrier_label="x" * 129)
    with pytest.raises(InvalidAsn, match="obce"):
        _parse(source_ref="http://evil")
