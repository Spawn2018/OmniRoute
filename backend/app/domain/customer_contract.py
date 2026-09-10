import binascii
import re
from base64 import b64decode

from app.domain.errors import InvalidCustomerContract

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_LABEL = 128
_MAX_REF = 256
_MAX_BLOB = 4096
_FIXTURE = "fixture://contract/"
_MANUAL = "tenant:manual"
_FIXTURE_BLOB = b"omniroute-fixture-opaque-v1"


def require_contract_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCustomerContract("oznaczenie musi być tekstem")
    token = raw.strip()
    if _CODE.fullmatch(token) is None:
        raise InvalidCustomerContract("oznaczenie: snake 2–32")
    return token


def require_shipper_label(raw: object) -> str:
    return _require_label(raw, "załadowca")


def require_their_customer_label(raw: object) -> str:
    return _require_label(raw, "odbiorca")


def _require_label(raw: object, token: str) -> str:
    if type(raw) is not str:
        raise InvalidCustomerContract(f"{token} musi być tekstem")
    label = raw.strip()
    if not label or len(label) > _MAX_LABEL:
        raise InvalidCustomerContract(f"{token}: tekst 1–128")
    return label


def require_contract_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCustomerContract("obce source_ref")
    token = raw.strip()
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidCustomerContract("obce wskazanie zapisu umowy klienta")
    if len(token) > _MAX_REF:
        raise InvalidCustomerContract("obce wskazanie zapisu umowy klienta za długie")
    return token


def fixture_opaque_blob() -> bytes:
    return _FIXTURE_BLOB


def require_opaque_fixture(raw: object) -> bool:
    if raw is None:
        return False
    if type(raw) is not bool:
        raise InvalidCustomerContract("opakowanie musi być flagą")
    return raw


def require_opaque_blob(raw: object) -> bytes | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidCustomerContract("opakowanie musi być tekstem")
    token = raw.strip()
    if not token:
        raise InvalidCustomerContract("opakowanie: base64 1–4096 B")
    try:
        blob = b64decode(token, validate=True)
    except binascii.Error as exc:
        raise InvalidCustomerContract("opakowanie: base64 1–4096 B") from exc
    if not blob or len(blob) > _MAX_BLOB:
        raise InvalidCustomerContract("opakowanie: base64 1–4096 B")
    return blob


def resolve_opaque_blob(*, opaque_fixture: object, opaque_blob: object) -> bytes | None:
    blob = require_opaque_blob(opaque_blob)
    if blob is not None:
        return blob
    if require_opaque_fixture(opaque_fixture):
        return _FIXTURE_BLOB
    return None
