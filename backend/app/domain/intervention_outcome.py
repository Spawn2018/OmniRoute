import re

from app.domain.errors import InvalidInterventionOutcome

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"contained", "rerouted", "claimed", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://intervention-outcome/"
_REF_CAP = 256


def parse_intervention_outcome_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidInterventionOutcome("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidInterventionOutcome("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidInterventionOutcome("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidInterventionOutcome(
            "rodzaj: contained, rerouted, claimed albo other",
        )
    if type(origin) is not str:
        raise InvalidInterventionOutcome("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidInterventionOutcome("obce wskazanie zapisu wyniku interwencji")
    if len(pointer) > _REF_CAP:
        raise InvalidInterventionOutcome(
            "obce wskazanie zapisu wyniku interwencji za długie",
        )
    return slug, token, pointer
