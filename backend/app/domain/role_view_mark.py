import re

from app.domain.errors import InvalidRoleViewMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_VIEW_KINDS = frozenset({"groupage", "ftl", "ocean", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://role-view-mark/"


def parse_role_view_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidRoleViewMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidRoleViewMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidRoleViewMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _VIEW_KINDS:
        raise InvalidRoleViewMark("rodzaj: groupage, ftl, ocean albo other")
    if type(origin) is not str:
        raise InvalidRoleViewMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidRoleViewMark("obce wskazanie zapisu znacznika widoku roli")
    if len(pointer) > 256:
        raise InvalidRoleViewMark("obce wskazanie zapisu znacznika widoku roli za długie")
    return slug, token, pointer
