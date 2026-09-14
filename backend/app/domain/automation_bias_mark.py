import re

from app.domain.errors import InvalidAutomationBiasMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"confirm", "delay", "review", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://automation-bias/"
_REF_CAP = 256


def parse_automation_bias_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidAutomationBiasMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidAutomationBiasMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidAutomationBiasMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidAutomationBiasMark(
            "rodzaj: confirm, delay, review albo other",
        )
    if type(origin) is not str:
        raise InvalidAutomationBiasMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidAutomationBiasMark(
            "obce wskazanie zapisu mitygacji automation bias",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidAutomationBiasMark(
            "obce wskazanie zapisu mitygacji automation bias za dlugie",
        )
    return slug, token, pointer
