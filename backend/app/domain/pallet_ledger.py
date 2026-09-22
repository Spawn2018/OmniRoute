import re
from uuid import UUID

from app.domain.errors import InvalidPalletLedger

_KINDS = frozenset({"chep", "lpr", "epal"})
_MAX_REF = 256
_FIXTURE = "fixture://pallet-ledger/"
_MANUAL = "tenant:manual"
_CODE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")


def require_ledger_party_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidPalletLedger("party_id musi być UUID")
    return raw


def require_movement_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPalletLedger("movement_code musi być tekstem")
    token = raw.strip()
    if not _CODE.match(token):
        raise InvalidPalletLedger("kod ruchu palet")
    return token


def require_ledger_pallet_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPalletLedger("pallet_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidPalletLedger("nieznany rodzaj palety")
    return token


def require_delta_count(raw: object) -> int:
    if type(raw) is bool or type(raw) is float:
        raise InvalidPalletLedger("liczba sztuk ruchu palet")
    if type(raw) is not int:
        raise InvalidPalletLedger("liczba sztuk ruchu palet")
    return raw


def require_ledger_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPalletLedger("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidPalletLedger("wskazanie zapisu ruchu palet")
    if len(token) > _MAX_REF:
        raise InvalidPalletLedger("wskazanie zapisu ruchu palet za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidPalletLedger("obce wskazanie zapisu ruchu palet")
    return token
