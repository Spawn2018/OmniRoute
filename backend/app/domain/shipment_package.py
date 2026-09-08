import re
from uuid import UUID

from app.domain.errors import InvalidShipmentPackage

_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_STATUSES = frozenset({"noted", "at_stop", "in_transit", "delivered"})
_MAX_REF = 256
_FIXTURE_REF = "fixture://shipment-package/"
_MANUAL = "tenant:manual"
_OMNI = "omni://shipment-package/"
_OMNI_FIXTURE = "fixture://omni-qr/"


def require_package_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidShipmentPackage("package_code musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE_PATTERN.fullmatch(token) is None:
        raise InvalidShipmentPackage("kod paczki: snake 2–32")
    return token


def require_package_uuid(raw: object, *, field: str) -> UUID:
    if type(raw) is not UUID:
        raise InvalidShipmentPackage(f"{field} musi być UUID")
    return raw


def require_package_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidShipmentPackage("package_status musi być tekstem")
    token = raw.strip()
    if token not in _STATUSES:
        raise InvalidShipmentPackage("nieznany status paczki")
    return token


def require_scan_token(raw: object, package_code: str) -> str:
    if type(raw) is not str:
        raise InvalidShipmentPackage("scan_token musi być tekstem")
    token = raw.strip()
    if token in {_OMNI + package_code, _OMNI_FIXTURE + package_code}:
        return token
    raise InvalidShipmentPackage("skan wymaga QR Omni")


def require_stop_on_shipment(shipment_id: UUID, stop_shipment_id: UUID) -> None:
    if shipment_id != stop_shipment_id:
        raise InvalidShipmentPackage("stop spoza trasy zlecenia")


def require_package_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidShipmentPackage("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidShipmentPackage("wskazanie zapisu paczki")
    if len(token) > _MAX_REF:
        raise InvalidShipmentPackage("wskazanie zapisu paczki za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE_REF):
        raise InvalidShipmentPackage("obce wskazanie zapisu paczki")
    return token
