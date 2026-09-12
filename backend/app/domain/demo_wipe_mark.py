import re

from app.domain.errors import InvalidDemoWipeMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_WIPE_KINDS = frozenset({"usun", "retain", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://demo-wipe-mark/"


def parse_demo_wipe_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidDemoWipeMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidDemoWipeMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidDemoWipeMark("rodzaj wipe musi być tekstem")
    token = kind.strip().lower()
    if token not in _WIPE_KINDS:
        raise InvalidDemoWipeMark(
            "rodzaj wipe: usun, retain albo other",
        )
    if type(origin) is not str:
        raise InvalidDemoWipeMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidDemoWipeMark(
            "obce wskazanie zapisu znacznika wipe demo",
        )
    if len(pointer) > 256:
        raise InvalidDemoWipeMark(
            "obce wskazanie zapisu znacznika wipe demo za długie",
        )
    return slug, token, pointer
