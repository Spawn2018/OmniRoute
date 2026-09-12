import re

from app.domain.errors import InvalidMailAcceptMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ACCEPT_KINDS = frozenset({"mailto", "confirm", "reject", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://mail-accept-mark/"


def parse_mail_accept_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidMailAcceptMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidMailAcceptMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidMailAcceptMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _ACCEPT_KINDS:
        raise InvalidMailAcceptMark("rodzaj: mailto, confirm, reject albo other")
    if type(origin) is not str:
        raise InvalidMailAcceptMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidMailAcceptMark("obce wskazanie zapisu znacznika Accept z maila")
    if len(pointer) > 256:
        raise InvalidMailAcceptMark("obce wskazanie zapisu znacznika Accept z maila za długie")
    return slug, token, pointer
