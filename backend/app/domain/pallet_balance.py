from uuid import UUID

from app.domain.errors import InvalidPalletBalance

_KINDS = frozenset({"chep", "lpr"})
_MAX_REF = 256
_FIXTURE = "fixture://pallet-balance/"
_MANUAL = "tenant:manual"


def require_balance_party_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidPalletBalance("party_id musi być UUID")
    return raw


def require_pallet_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPalletBalance("pallet_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidPalletBalance("nieznany rodzaj palety")
    return token


def require_unit_count(raw: object) -> int:
    if type(raw) is bool or type(raw) is float:
        raise InvalidPalletBalance("liczba sztuk palet")
    if type(raw) is not int:
        raise InvalidPalletBalance("liczba sztuk palet")
    if raw < 0:
        raise InvalidPalletBalance("liczba sztuk palet nieujemna")
    return raw


def require_balance_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidPalletBalance("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidPalletBalance("wskazanie zapisu salda palet")
    if len(token) > _MAX_REF:
        raise InvalidPalletBalance("wskazanie zapisu salda palet za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidPalletBalance("obce wskazanie zapisu salda palet")
    return token
