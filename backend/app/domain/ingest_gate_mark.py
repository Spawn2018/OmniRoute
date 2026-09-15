import re

from app.domain.errors import InvalidIngestGateMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"truth", "owner", "exception", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://ingest-gate-mark/"
_REF_CAP = 256


def parse_ingest_gate_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidIngestGateMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidIngestGateMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidIngestGateMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidIngestGateMark(
            "rodzaj: truth, owner, exception albo other",
        )
    if type(origin) is not str:
        raise InvalidIngestGateMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidIngestGateMark(
            "obce wskazanie zapisu mitygacji brama ingest",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidIngestGateMark(
            "obce wskazanie zapisu mitygacji brama ingest za dlugie",
        )
    return slug, token, pointer
