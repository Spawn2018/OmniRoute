import re

from app.domain.errors import InvalidRagSopMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_SCOPE_KINDS = frozenset({"sop", "adr", "mail", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://rag-sop-mark/"


def parse_rag_sop_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidRagSopMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidRagSopMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidRagSopMark("zakres musi być tekstem")
    token = kind.strip().lower()
    if token not in _SCOPE_KINDS:
        raise InvalidRagSopMark("zakres: sop, adr, mail albo other")
    if type(origin) is not str:
        raise InvalidRagSopMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidRagSopMark("obce wskazanie zapisu znacznika zakresu RAG")
    if len(pointer) > 256:
        raise InvalidRagSopMark("obce wskazanie zapisu znacznika zakresu RAG za długie")
    return slug, token, pointer
