import re

from app.domain.errors import InvalidImpactScenario

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_PREFIX = "fixture://impact-scenario/"
_REF_CAP = 256
_LABEL_CAP = 64


def parse_impact_scenario_row(
    code: object, chain_label: object, origin: object
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidImpactScenario("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidImpactScenario("oznaczenie: snake 2–32")
    if type(chain_label) is not str:
        raise InvalidImpactScenario("etykieta musi być tekstem")
    label = chain_label.strip()
    if not label or len(label) > _LABEL_CAP:
        raise InvalidImpactScenario("etykieta: tekst 1–64")
    if type(origin) is not str:
        raise InvalidImpactScenario("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidImpactScenario("obce wskazanie zapisu scenariusza skutku")
    if len(pointer) > _REF_CAP:
        raise InvalidImpactScenario("obce wskazanie zapisu scenariusza skutku za długie")
    return slug, label, pointer
