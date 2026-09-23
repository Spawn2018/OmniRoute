import re

from app.domain.errors import InvalidHandoverBindMark

_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ALLOWED = frozenset({"note", "board", "shift", "other"})
_MANUAL_REF = "tenant:manual"
_FIXTURE = "fixture://handover-bind/"
_MAX_REF = 256


def parse_handover_bind_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidHandoverBindMark("kod musi być tekstem")
    slug = code.strip()
    if _CODE_RE.fullmatch(slug) is None:
        raise InvalidHandoverBindMark("kod: snake 2–32")
    if type(kind) is not str:
        raise InvalidHandoverBindMark("wiązanie musi być tekstem")
    token = kind.strip().lower()
    if token not in _ALLOWED:
        raise InvalidHandoverBindMark(
            "wiązanie: note, board, shift albo other",
        )
    if type(origin) is not str:
        raise InvalidHandoverBindMark("obce wskazanie wiązania przekazania")
    pointer = origin.strip()
    if pointer != _MANUAL_REF and not pointer.startswith(_FIXTURE):
        raise InvalidHandoverBindMark("obce wskazanie wiązania przekazania")
    if len(pointer) > _MAX_REF:
        raise InvalidHandoverBindMark("wskazanie wiązania przekazania za długie")
    return slug, token, pointer
