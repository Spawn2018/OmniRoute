import re

from app.domain.errors import InvalidOtifMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_SCOPES = frozenset({"pickup", "delivery", "sku"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://otif-mark/"
_REF_CAP = 256


def parse_otif_mark_row(
    code: object, scope: object, origin: object
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidOtifMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidOtifMark("oznaczenie: snake 2–32")
    if type(scope) is not str:
        raise InvalidOtifMark("zakres musi być tekstem")
    kind = scope.strip().lower()
    if kind not in _SCOPES:
        raise InvalidOtifMark("zakres: pickup, delivery albo sku")
    if type(origin) is not str:
        raise InvalidOtifMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidOtifMark("obce wskazanie zapisu znacznika OTIF")
    if len(pointer) > _REF_CAP:
        raise InvalidOtifMark("obce wskazanie zapisu znacznika OTIF za długie")
    return slug, kind, pointer
