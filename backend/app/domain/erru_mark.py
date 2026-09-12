import re

from app.domain.errors import InvalidErruMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_CHECK_KINDS = frozenset({"to_verify", "clear", "hit", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://erru-mark/"


def parse_erru_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidErruMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidErruMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidErruMark("sprawdzenie musi być tekstem")
    token = kind.strip().lower()
    if token not in _CHECK_KINDS:
        raise InvalidErruMark("sprawdzenie: to_verify, clear, hit albo other")
    if type(origin) is not str:
        raise InvalidErruMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidErruMark("obce wskazanie zapisu znacznika ERRU")
    if len(pointer) > 256:
        raise InvalidErruMark("obce wskazanie zapisu znacznika ERRU za długie")
    return slug, token, pointer
