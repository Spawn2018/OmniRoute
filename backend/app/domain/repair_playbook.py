import re

from app.domain.errors import InvalidRepairPlaybook

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"contain", "reroute", "claim", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://repair-playbook/"
_REF_CAP = 256


def parse_repair_playbook_row(
    code: object, kind: object, origin: object
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidRepairPlaybook("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidRepairPlaybook("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidRepairPlaybook("postawa musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidRepairPlaybook("postawa: contain, reroute, claim albo other")
    if type(origin) is not str:
        raise InvalidRepairPlaybook("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidRepairPlaybook("obce wskazanie zapisu playbooka naprawy")
    if len(pointer) > _REF_CAP:
        raise InvalidRepairPlaybook("obce wskazanie zapisu playbooka naprawy za długie")
    return slug, token, pointer
