from uuid import uuid4

import pytest

from app.domain.errors import InvalidShipmentPackage
from app.domain.shipment_package import (
    require_consignment_on_shipment,
    require_package_code,
    require_package_source_ref,
    require_package_status,
    require_scan_token,
    require_stop_on_shipment,
)


def test_shipment_package_allowlists() -> None:
    assert require_package_code(" BOX-1 ") == "box_1"
    assert require_package_status("at_stop") == "at_stop"
    assert require_scan_token("omni://shipment-package/box_1", "box_1") == (
        "omni://shipment-package/box_1"
    )
    assert require_scan_token("fixture://omni-qr/box_1", "box_1") == "fixture://omni-qr/box_1"
    assert require_package_source_ref("fixture://shipment-package/a") == (
        "fixture://shipment-package/a"
    )
    same = uuid4()
    require_stop_on_shipment(same, same)
    require_consignment_on_shipment(same, same)


def test_shipment_package_rejects_foreign_scan_and_stop() -> None:
    with pytest.raises(InvalidShipmentPackage, match="QR Omni"):
        require_scan_token("barcode-123", "box_1")
    with pytest.raises(InvalidShipmentPackage, match="trasy"):
        require_stop_on_shipment(uuid4(), uuid4())
    with pytest.raises(InvalidShipmentPackage, match="przesyłka"):
        require_consignment_on_shipment(uuid4(), uuid4())
    with pytest.raises(InvalidShipmentPackage, match="status"):
        require_package_status("lost")
    with pytest.raises(InvalidShipmentPackage, match="obce"):
        require_package_source_ref("https://evil.example/pkg")
    with pytest.raises(InvalidShipmentPackage, match="snake"):
        require_package_code("1box")
