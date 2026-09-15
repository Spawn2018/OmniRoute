import re

from app.domain.errors import InvalidComplianceProgramMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"draft", "review", "signed", "exempt", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://compliance-program/"
_REF_CAP = 256


def parse_compliance_program_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidComplianceProgramMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidComplianceProgramMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidComplianceProgramMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidComplianceProgramMark(
            "rodzaj: draft, review, signed, exempt albo other",
        )
    if type(origin) is not str:
        raise InvalidComplianceProgramMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidComplianceProgramMark(
            "obce wskazanie zapisu stancji programu zgodnosci",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidComplianceProgramMark(
            "obce wskazanie zapisu stancji programu zgodnosci za dlugie",
        )
    return slug, token, pointer
