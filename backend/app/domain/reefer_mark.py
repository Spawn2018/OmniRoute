import re

from app.domain.errors import InvalidReeferMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_REEFER_KINDS = frozenset({"reefer", "setpoint", "genset", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://reefer-mark/"


def parse_reefer_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidReeferMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidReeferMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidReeferMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _REEFER_KINDS:
        raise InvalidReeferMark("rodzaj: reefer, setpoint, genset albo other")
    if type(origin) is not str:
        raise InvalidReeferMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidReeferMark("obce wskazanie zapisu znacznika reefer")
    if len(pointer) > 256:
        raise InvalidReeferMark("obce wskazanie zapisu znacznika reefer za długie")
    return slug, token, pointer
