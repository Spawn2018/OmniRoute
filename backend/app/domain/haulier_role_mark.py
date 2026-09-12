import re

from app.domain.errors import InvalidHaulierRoleMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"booked", "actual", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://haulier-role-mark/"


def parse_haulier_role_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidHaulierRoleMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidHaulierRoleMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidHaulierRoleMark("rodzaj roli musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidHaulierRoleMark(
            "rodzaj roli: booked, actual albo other",
        )
    if type(origin) is not str:
        raise InvalidHaulierRoleMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidHaulierRoleMark(
            "obce wskazanie zapisu znacznika roli przewoznika",
        )
    if len(pointer) > 256:
        raise InvalidHaulierRoleMark(
            "obce wskazanie zapisu znacznika roli przewoznika za długie",
        )
    return slug, token, pointer
