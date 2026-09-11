import re

from app.domain.errors import InvalidCompanyMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"hq", "branch", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://company-mark/"
_REF_CAP = 256


def parse_company_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCompanyMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCompanyMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCompanyMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCompanyMark(
            "rodzaj: hq, branch albo other",
        )
    if type(origin) is not str:
        raise InvalidCompanyMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCompanyMark("obce wskazanie zapisu znacznika spółki")
    if len(pointer) > _REF_CAP:
        raise InvalidCompanyMark("obce wskazanie zapisu znacznika spółki za długie")
    return slug, token, pointer
