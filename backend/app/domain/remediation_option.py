import re

from app.domain.errors import InvalidRemediationOption

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"rebook", "wait", "claim", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://remediation-option/"
_REF_CAP = 256


def parse_remediation_option_row(
    code: object, kind: object, origin: object
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidRemediationOption("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidRemediationOption("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidRemediationOption("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidRemediationOption("rodzaj: rebook, wait, claim albo other")
    if type(origin) is not str:
        raise InvalidRemediationOption("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidRemediationOption("obce wskazanie zapisu opcji naprawy")
    if len(pointer) > _REF_CAP:
        raise InvalidRemediationOption("obce wskazanie zapisu opcji naprawy za długie")
    return slug, token, pointer
