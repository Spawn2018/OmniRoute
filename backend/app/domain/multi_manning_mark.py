import re

from app.domain.errors import InvalidMultiManningMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANNING_KINDS = frozenset({"dual", "relay", "team", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://multi-manning-mark/"


def parse_multi_manning_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidMultiManningMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidMultiManningMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidMultiManningMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _MANNING_KINDS:
        raise InvalidMultiManningMark("rodzaj: dual, relay, team albo other")
    if type(origin) is not str:
        raise InvalidMultiManningMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidMultiManningMark("obce wskazanie zapisu znacznika reefer")
    if len(pointer) > 256:
        raise InvalidMultiManningMark("obce wskazanie zapisu znacznika reefer za długie")
    return slug, token, pointer
