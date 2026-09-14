import re

from app.domain.errors import InvalidRiskRegisterMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"open", "mitigated", "accepted", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://risk-register/"
_REF_CAP = 256


def parse_risk_register_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidRiskRegisterMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidRiskRegisterMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidRiskRegisterMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidRiskRegisterMark(
            "rodzaj: open, mitigated, accepted albo other",
        )
    if type(origin) is not str:
        raise InvalidRiskRegisterMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidRiskRegisterMark(
            "obce wskazanie zapisu rejestru ryzyka",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidRiskRegisterMark(
            "obce wskazanie zapisu rejestru ryzyka za dlugie",
        )
    return slug, token, pointer
