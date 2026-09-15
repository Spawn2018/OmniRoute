import re

from app.domain.errors import InvalidCrmPipelineMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"stage", "won", "lost", "hold", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://crm-pipeline-mark/"
_REF_CAP = 256


def parse_crm_pipeline_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCrmPipelineMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCrmPipelineMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCrmPipelineMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCrmPipelineMark("rodzaj: stage, won, lost, hold albo other")
    if type(origin) is not str:
        raise InvalidCrmPipelineMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCrmPipelineMark("obce wskazanie zapisu etapu CRM")
    if len(pointer) > _REF_CAP:
        raise InvalidCrmPipelineMark("obce wskazanie zapisu etapu CRM za długie")
    return slug, token, pointer
