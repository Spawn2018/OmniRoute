import re

from app.domain.errors import InvalidPalletSynchroMark

_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ALLOWED = frozenset({"aligned", "drift", "held", "other"})
_MANUAL_REF = "tenant:manual"
_FIXTURE = "fixture://pallet-synchro/"
_MAX_REF = 256


def parse_pallet_synchro_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPalletSynchroMark("kod musi być tekstem")
    slug = code.strip()
    if _CODE_RE.fullmatch(slug) is None:
        raise InvalidPalletSynchroMark("kod: snake 2–32")
    if type(kind) is not str:
        raise InvalidPalletSynchroMark("synchro musi być tekstem")
    token = kind.strip().lower()
    if token not in _ALLOWED:
        raise InvalidPalletSynchroMark("synchro: aligned, drift, held albo other")
    if type(origin) is not str:
        raise InvalidPalletSynchroMark("obce wskazanie synchro palet")
    pointer = origin.strip()
    if pointer != _MANUAL_REF and not pointer.startswith(_FIXTURE):
        raise InvalidPalletSynchroMark("obce wskazanie synchro palet")
    if len(pointer) > _MAX_REF:
        raise InvalidPalletSynchroMark("wskazanie synchro palet za długie")
    return slug, token, pointer
