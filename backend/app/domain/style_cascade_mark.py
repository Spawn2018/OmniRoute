import re

from app.domain.errors import InvalidStyleCascadeMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset(
    {
        "global",
        "company",
        "department",
        "user",
        "customer",
        "person",
        "context",
        "other",
    },
)
_MANUAL = "tenant:manual"
_PREFIX = "fixture://style-cascade/"
_REF_CAP = 256


def parse_style_cascade_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidStyleCascadeMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidStyleCascadeMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidStyleCascadeMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidStyleCascadeMark(
            "rodzaj: global, company, department, user, "
            "customer, person, context albo other",
        )
    if type(origin) is not str:
        raise InvalidStyleCascadeMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidStyleCascadeMark(
            "obce wskazanie zapisu poziomu kaskady stylu",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidStyleCascadeMark(
            "obce wskazanie zapisu poziomu kaskady stylu za dlugie",
        )
    return slug, token, pointer
