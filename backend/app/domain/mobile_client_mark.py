import re

from app.domain.errors import InvalidMobileClientMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_CLIENT_KINDS = frozenset({"ios", "android", "ota", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://mobile-client-mark/"


def parse_mobile_client_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidMobileClientMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidMobileClientMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidMobileClientMark("klient musi być tekstem")
    token = kind.strip().lower()
    if token not in _CLIENT_KINDS:
        raise InvalidMobileClientMark("klient: ios, android, ota albo other")
    if type(origin) is not str:
        raise InvalidMobileClientMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidMobileClientMark("obce wskazanie zapisu znacznika klienta mobilnego")
    if len(pointer) > 256:
        raise InvalidMobileClientMark("obce wskazanie zapisu znacznika klienta mobilnego za długie")
    return slug, token, pointer
