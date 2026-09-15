import re

from app.domain.errors import InvalidKpiDefinitionMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"otd", "otif", "custom", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://kpi-definition-mark/"
_REF_CAP = 256


def parse_kpi_definition_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidKpiDefinitionMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidKpiDefinitionMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidKpiDefinitionMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidKpiDefinitionMark(
            "rodzaj: otd, otif, custom albo other",
        )
    if type(origin) is not str:
        raise InvalidKpiDefinitionMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidKpiDefinitionMark(
            "obce wskazanie zapisu definicji KPI",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidKpiDefinitionMark(
            "obce wskazanie zapisu definicji KPI za dlugie",
        )
    return slug, token, pointer
