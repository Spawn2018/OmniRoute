import re

from app.domain.errors import InvalidDemoSimMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_SIM_KINDS = frozenset({"fleet_150", "months_10", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://demo-sim-mark/"


def parse_demo_sim_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidDemoSimMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidDemoSimMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidDemoSimMark("rodzaj sim musi być tekstem")
    token = kind.strip().lower()
    if token not in _SIM_KINDS:
        raise InvalidDemoSimMark(
            "rodzaj sim: fleet_150, months_10 albo other",
        )
    if type(origin) is not str:
        raise InvalidDemoSimMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidDemoSimMark(
            "obce wskazanie zapisu znacznika demo sim",
        )
    if len(pointer) > 256:
        raise InvalidDemoSimMark(
            "obce wskazanie zapisu znacznika demo sim za długie",
        )
    return slug, token, pointer
