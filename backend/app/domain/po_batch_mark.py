import re

from app.domain.errors import InvalidPoBatchMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_BATCH_KINDS = frozenset({"batch", "lot", "serial", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://po-batch-mark/"


def parse_po_batch_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPoBatchMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidPoBatchMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidPoBatchMark("rodzaj batch musi być tekstem")
    token = kind.strip().lower()
    if token not in _BATCH_KINDS:
        raise InvalidPoBatchMark(
            "rodzaj batch: batch, lot, serial albo other",
        )
    if type(origin) is not str:
        raise InvalidPoBatchMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidPoBatchMark(
            "obce wskazanie zapisu znacznika po batch",
        )
    if len(pointer) > 256:
        raise InvalidPoBatchMark(
            "obce wskazanie zapisu znacznika po batch za długie",
        )
    return slug, token, pointer
