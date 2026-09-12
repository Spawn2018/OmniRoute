import re

from app.domain.errors import InvalidSwitchBlLoiMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"bl", "loi", "switch", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://switch-bl-loi-mark/"
_REF_CAP = 256


def parse_switch_bl_loi_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidSwitchBlLoiMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidSwitchBlLoiMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidSwitchBlLoiMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidSwitchBlLoiMark(
            "rodzaj: bl, loi, switch albo other",
        )
    if type(origin) is not str:
        raise InvalidSwitchBlLoiMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidSwitchBlLoiMark("obce wskazanie zapisu znacznika switch BL/LOI")
    if len(pointer) > _REF_CAP:
        raise InvalidSwitchBlLoiMark(
            "obce wskazanie zapisu znacznika switch BL/LOI za długie",
        )
    return slug, token, pointer
