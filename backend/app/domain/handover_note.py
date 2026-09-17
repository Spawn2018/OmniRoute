import re

from app.domain.errors import InvalidHandoverNote

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_PREFIX = "fixture://handover-note/"
_REF_CAP = 256
_FIELD_CAP = 2000


def _require_field(label: str, raw: object) -> str:
    if type(raw) is not str:
        raise InvalidHandoverNote(f"{label} musi być tekstem")
    text = raw.strip()
    if not text:
        raise InvalidHandoverNote(f"{label} nie może być puste")
    if len(text) > _FIELD_CAP:
        raise InvalidHandoverNote(f"{label} za długie")
    return text


def parse_handover_note_row(
    code: object,
    situation: object,
    background: object,
    assessment: object,
    recommendation: object,
    origin: object,
) -> tuple[str, str, str, str, str, str]:
    if type(code) is not str:
        raise InvalidHandoverNote("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidHandoverNote("oznaczenie: snake 2–32")
    sit = _require_field("sytuacja", situation)
    back = _require_field("tło", background)
    assess = _require_field("ocena", assessment)
    rec = _require_field("rekomendacja", recommendation)
    if type(origin) is not str:
        raise InvalidHandoverNote("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidHandoverNote("obce wskazanie zapisu notatki SBAR")
    if len(pointer) > _REF_CAP:
        raise InvalidHandoverNote("obce wskazanie zapisu notatki SBAR za długie")
    return slug, sit, back, assess, rec, pointer
