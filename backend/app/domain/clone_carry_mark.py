import re

from app.domain.errors import InvalidCloneCarryMark

_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ALLOWED = frozenset({"carry", "held", "skip", "other"})
_MANUAL_REF = "tenant:manual"
_FIXTURE = "fixture://clone-carry/"
_MAX_REF = 256


def parse_clone_carry_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCloneCarryMark("kod musi być tekstem")
    slug = code.strip()
    if _CODE_RE.fullmatch(slug) is None:
        raise InvalidCloneCarryMark("kod: snake 2–32")
    if type(kind) is not str:
        raise InvalidCloneCarryMark("carry musi być tekstem")
    token = kind.strip().lower()
    if token not in _ALLOWED:
        raise InvalidCloneCarryMark("carry: carry, held, skip albo other")
    if type(origin) is not str:
        raise InvalidCloneCarryMark("obce wskazanie carry przy klonie")
    pointer = origin.strip()
    if pointer != _MANUAL_REF and not pointer.startswith(_FIXTURE):
        raise InvalidCloneCarryMark("obce wskazanie carry przy klonie")
    if len(pointer) > _MAX_REF:
        raise InvalidCloneCarryMark("wskazanie carry przy klonie za długie")
    return slug, token, pointer
